from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

connection_string = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:albatross21.database.windows.net,1433;Database=albatross21;Uid=rua;Pwd=Myh.1059331302;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
connection_url = URL.create(
    "mssql+pyodbc",
    username="rua",
    password="Myh.1059331302",
    host="tcp:albatross21.database.windows.net",
    port=1433,
    database="albatross21",
    query={
        "Connection Timeout": "30",
        "driver": "ODBC Driver 18 for SQL Server",
        "Encrypt": "yes",
        "TrustServerCertificate": "yes",
    },
)

engine = create_engine(connection_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
