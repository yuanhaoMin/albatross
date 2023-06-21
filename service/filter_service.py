import json
import logging
import openai
from constant.openai_constant import OPENAI_TIMEOUT_MSG
from fastapi import HTTPException
from openai.error import Timeout
from service.setting_service import get_api_key_settings


logger = logging.getLogger(__name__)


def openai_check_harmful_content(message: str) -> None:
    openai.api_key = get_api_key_settings().openai_api_key
    functions = [
        {
            "name": "check_harmful_content",
            "description": "Access the level of correlation between the input and Chinese political, violent, or sexual content",
            "parameters": {
                "type": "object",
                "properties": {
                    "level": {
                        "type": "string",
                        "description": "The degree of the input's association with political, violent, or sexual content",
                        "enum": ["none", "low", "high"],
                    }
                },
                "required": ["level"],
            },
        }
    ]
    max_retries = 2
    retry_count = 0
    timeout_log_message = OPENAI_TIMEOUT_MSG.format(
        function_name=openai_check_harmful_content.__name__
    )
    while True:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=[{"role": "user", "content": message}],
                functions=functions,
                function_call={"name": "check_harmful_content"},
                request_timeout=2,
            )
            data = json.loads(
                response["choices"][0]["message"]["function_call"]["arguments"]
            )
            level = data["level"]
            if level == "high":
                raise HTTPException(status_code=418, detail="Harmful content detected")
            break
        except Timeout:
            retry_count += 1
            if retry_count > max_retries:
                raise HTTPException(
                    status_code=504,
                    detail=timeout_log_message,
                )
            else:
                logger.warn(timeout_log_message)
                continue
