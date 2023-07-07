from configuration import setting
from functools import lru_cache


@lru_cache()
def get_api_key_settings():
    return setting.api_key_settings()


@lru_cache()
def get_open_ai_api(model: str = None):
    if model == "gpt-4":
        return "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"
    else:
        return "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"


@lru_cache()
def get_db_settings():
    return setting.db_settings()
