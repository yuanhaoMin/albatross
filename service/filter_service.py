import json
import openai
from fastapi import HTTPException
from service.setting_service import get_api_key_settings


def openai_check_harmful_content(message: str) -> bool:
    openai.api_key = get_api_key_settings().openai_api_key
    functions = [
        {
            "name": "is_input_harmful",
            "description": "Predict if the input is related to political/violent/sexual",
            "parameters": {
                "type": "object",
                "properties": {
                    "result": {
                        "type": "boolean",
                        "description": "If the input is related to political/violent/sexual",
                    }
                },
                "required": ["result"],
            },
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[{"role": "user", "content": message}],
        functions=functions,
        function_call="auto",
        timeout=3,
    )
    if response["choices"][0]["finish_reason"] == "function_call":
        data = json.loads(
            response["choices"][0]["message"]["function_call"]["arguments"]
        )
        is_harmful = bool(data["result"])
        if is_harmful:
            raise HTTPException(status_code=418, detail="Harmful content detected")
