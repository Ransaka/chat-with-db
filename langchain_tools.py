from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Type
from db_config import sql_connection
from sqlalchemy import text
import pandas as pd 
import uuid, os
from dotenv import load_dotenv

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_KEY")

TABLE_SCHEMA = """Table DDL is,

CREATE TABLE `employee_usage_details` (
  `employee_id` bigint DEFAULT NULL,
  `score` bigint DEFAULT NULL,
  `product` text,
  `date` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

Sample records are,

'|    |   employee_id |   score | product   | date                |\n|---:|--------------:|--------:|:----------|:--------------------|\n|  0 |           100 |       1 | gmail     | 2017-11-13 00:00:00 |\n|  1 |           101 |      90 | calendar  | 2017-11-13 00:00:00 |\n|  2 |           102 |      16 | hangouts  | 2017-11-13 00:00:00 |\n|  3 |           103 |      90 | calendar  | 2017-11-12 00:00:00 |\n|  4 |           104 |       1 | gmail     | 2017-11-10 00:00:00 |'
"""

def save_file(sql, engine):
    df = pd.read_sql(sql=sql, con=engine.connect())
    file_name = f"{(uuid.uuid4())}.csv"
    df.to_csv(file_name)
    return file_name

class SQLQueryInputs(BaseModel):
    """Inputs for SQLqueryGeneratorTool"""
    question: str = Field(description="User question to be convert into SQL query")

class SQLqueryGeneratorTool(BaseTool):
    name = "sql-generator-tool"
    description = "SQL code generation tool. Usefull when wants to generate SQL code from given user question."
    args_schema: Type[BaseModel] = SQLQueryInputs

    def _run(self, question: str):
        template = f"""
        You are a supportive Q&A bot. Below you have given user question your task is to convert that into SQL code.
        table schema: {TABLE_SCHEMA}
        Question: {question}
        """
        llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", verbose=True, api_key=OPENAI_KEY)
        return llm.invoke(input=template)

    def _arun(self, url: str):
        raise NotImplementedError("error here")
    
class SQLQueryValidatorInput(BaseModel):
    """Inputs for SQLQueryValidator tool"""
    sql_code: str = Field(description="LLM Agent generated response")
    
class SQLQueryValidatorTool(BaseTool):
    name = "sql-query-validator-tool"
    description = "SQL code validation tool. Usefull when wants to validate SQL code."
    args_schema: Type[BaseModel] = SQLQueryValidatorInput

    def _run(self, sql_code: str):
        template = f"""
        You are supportive query validator your task is to validate and return answers based on below steps given llm agent responses. 
        - Should return SQL code ONLY.

        Ex: LLM agent response: The SQL query to find the total number of employees is:\n\n```sql\nSELECT COUNT(DISTINCT employee_id) AS total_employees\nFROM employee_usage_details;\n```
            Response should be: SELECT COUNT(DISTINCT employee_id) AS total_employees\nFROM employee_usage_details;
        LLM Generated Response: {sql_code}
        """
        llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", verbose=True, api_key=OPENAI_KEY)
        return llm.invoke(input=template),sql_code

    def _arun(self, url: str):
        raise NotImplementedError("error here")
    

class SQLQueryExecutorInput(BaseModel):
    """Inputs for SQLQueryExecutorInput tool"""
    sql_code: str = Field(description="SQL Code to be executed.")
    original_question:str = Field(description="Unprocessed agent response to finalize end result.")
    
class SQLQueryExecutorTool(BaseTool):
    name = "sql-query-executor-tool"
    description = "SQL code executor tool. Usefull when wants to execute SQL code."
    args_schema: Type[BaseModel] = SQLQueryExecutorInput

    def _run(self, sql_code: str, original_question:str):
        engine = sql_connection()
        llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", verbose=True, api_key=OPENAI_KEY)
        template = f"""
        Analyze user question and understand whether user wants output as file or not based on below rules.
        1./ If user explicitly ask for file user return "Yes" Otherwise "No"
        2./ If user ask for 20+ records then return "Yes" Otherwise "No". You are free to breakdown and think step by step.
        User Question: {original_question}
        """
        is_file = llm.invoke(input=template).content
        print(f"{is_file=}")
        if "Yes" in is_file:
            file_name = save_file(sql=sql_code, engine=engine)
            return {"output_type":"csv","output_file_name":file_name}
        else:
            result = engine.connect().execute(text(sql_code)).fetchall()
            return {"Executor Result":result,"Unprocessed LLM response":original_question}
    def _arun(self, url: str):
        raise NotImplementedError("error here")
