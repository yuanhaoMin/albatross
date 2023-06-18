from pydantic import BaseSettings


class api_key_settings(BaseSettings):
    openai_api_key: str
    serper_api_key: str

    class Config:
        env_file = ".env"


class db_settings(BaseSettings):
    mssql_connection_string: str

    class Config:
        env_file = ".env"
