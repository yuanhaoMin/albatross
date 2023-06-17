from pydantic import BaseSettings


class alipay_settings(BaseSettings):
    alipay_dev_mode: bool

    class Config:
        env_file = ".env"


class api_key_settings(BaseSettings):
    openai_api_key: str
    serper_api_key: str

    class Config:
        env_file = ".env"


class db_settings(BaseSettings):
    mssql_connection_string: str

    class Config:
        env_file = ".env"
