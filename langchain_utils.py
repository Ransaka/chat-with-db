from langchain.schema import SystemMessage
from langchain_openai import ChatOpenAI
from langchain_tools import SQLqueryGeneratorTool, OPENAI_KEY, SQLQueryValidatorTool, SQLQueryExecutorTool
from langchain.agents import initialize_agent, AgentType, create_structured_chat_agent
from langchain.tools import Tool

system_message = SystemMessage(
    content="""You are support Q&A bot optimized for SQL query generation, file writing and responding to them. If you are unable to answer specific user query you 
    are free to respond with 'I dont know'.

        Please make sure you complete the objective above with the following rules:
        1/ Your job is to first breakdown your execution plan using available tools. Every tool may or may not be required to complete task. Available tools are SQL query generator, SQL query validator, SQL query executor, file writer and response generator.
        2/ You should use the SQL validator and SQL executor tools if you decided to use SQL generator tool.
        3/ Use file writer tools if user ask for file directly. Otherwise use response generator tool.
        """
)

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", verbose=True, api_key=OPENAI_KEY)
agent_kwargs = {
    "system_message": system_message,
}

tools = [SQLqueryGeneratorTool(), 
         SQLQueryValidatorTool(),
         SQLQueryExecutorTool()
    ]
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
    agent_kwargs=agent_kwargs,
)
# response = agent.invoke({"input":"Give me most recent 90 records for user 101."})
# print(response)
