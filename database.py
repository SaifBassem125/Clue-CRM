from pyodbc import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config
from urllib.parse import quote

# Set up the base class for declarative models
Base = declarative_base()

# Set up the database engine and session
DATABASE_URL_SQL_SERVER = f"mssql+pyodbc://{config('DB_USER')}:{quote(config('DB_PASSWORD'))}@{config('DB_HOST')}:{config('DB_PORT')}/{config('DB_NAME')}?driver=ODBC+Driver+18+for+SQL+Server&ConnectionTimeout=30&LoginTimeout=30&encrypt=no&trustServerCertificate=yes"
engine_sql_server = create_engine(DATABASE_URL_SQL_SERVER)

SessionSQLServer = sessionmaker(bind=engine_sql_server)

# Set up the database engine and session
DATABASE_URL_MAPPING_SERVER = f"mssql+pyodbc://{config('DB_USER')}:{quote(config('DB_PASSWORD'))}@{config('DB_HOST')}:{config('DB_PORT')}/{config('DB_MAPPING_NAME')}?driver=ODBC+Driver+18+for+SQL+Server&ConnectionTimeout=30&LoginTimeout=30&encrypt=no&trustServerCertificate=yes"
engine_sql_mapping_server = create_engine(DATABASE_URL_MAPPING_SERVER)

SessionSQLServerMapping = sessionmaker(bind=engine_sql_mapping_server)


# # Set up the PostgreSQL database engine and session
# DATABASE_URL_POSTGRES = f"postgresql://{config('PG_USER')}:{quote(config('PG_PASSWORD'))}@{config('PG_HOST')}:{config('PG_PORT')}/{config('PG_NAME')}"
# engine_postgres = create_engine(DATABASE_URL_POSTGRES)

# SessionPostgres = sessionmaker(bind=engine_postgres)

# Function to get a new session for SQL Server
def get_session_sql_server():
    return SessionSQLServer()

# Function to get a new session for SQL Server
def get_session_mapping():
    return SessionSQLServerMapping()

# # Function to get a new session for PostgreSQL
# def get_session_postgres():
#     return SessionPostgres()
