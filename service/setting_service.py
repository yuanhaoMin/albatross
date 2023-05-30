from configuration import setting
from functools import lru_cache


@lru_cache()
def get_api_key_settings():
    return setting.api_key_settings()


def get_db_settings():
    return setting.db_settings()
