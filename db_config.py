import os
from sqlalchemy import create_engine

DB_CONFIG = {
    "COMMON":{
        "DATABASE_HOST":os.environ.get("DATABASE_HOST", "localhost").strip(),#host.docker.internal
        "DATABASE_PORT":int(os.environ.get("DATABASE_PORT", "3306").strip()),
        "DATABASE_NAME": os.environ.get("SOURCE_DATABASE_NAME", "db_name").strip(),
        "DATABASE_PASSWORD": os.environ.get("DATABASE_PASSWORD", "11111111").strip(),
        "DATABASE_USERNAME": os.environ.get("DATABASE_USERNAME","root").strip()
    }
}

def sql_connection():
    """This only for write with pandas"""
    return create_engine(
            "mysql+pymysql://" 
            + DB_CONFIG['COMMON']['DATABASE_USERNAME']                 # database username
            + ":" + DB_CONFIG['COMMON']['DATABASE_PASSWORD']           # database password
            + "@" + DB_CONFIG['COMMON']['DATABASE_HOST']               # database host
            + ":" + str(DB_CONFIG['COMMON']['DATABASE_PORT'])          # database port     
            + "/" + DB_CONFIG['COMMON']['DATABASE_NAME']               # database name
        )

def sql_connection():
    """This only for write with pandas"""
    return create_engine(
            "mysql+pymysql://" 
            + DB_CONFIG['COMMON']['DATABASE_USERNAME']                 # database username
            + ":" + DB_CONFIG['COMMON']['DATABASE_PASSWORD']           # database password
            + "@" + DB_CONFIG['COMMON']['DATABASE_HOST']               # database host
            + ":" + str(DB_CONFIG['COMMON']['DATABASE_PORT'])          # database port     
            + "/" + DB_CONFIG['COMMON']['DATABASE_NAME']               # database name
        )
