import json
import logging
import openai
from constant.openai_constant import OPENAI_TIMEOUT_MSG
from fastapi import HTTPException
from openai.error import Timeout

logger = logging.getLogger(__name__)


def determine_api(prompt: str) -> str:
    functions = [
        {
            "name": "navigation",
            "description": "导航至某个页面",
            "parameters": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "description": "页面: 轨迹大屏, 数据大屏, 访客列表",
                        "enum": ["data", "track", "visitor"],
                    }
                },
                "required": ["type"],
            },
        },
    ]
    max_retries = 2
    retry_count = 0
    timeout_log_message = OPENAI_TIMEOUT_MSG.format(
        function_name=determine_api.__name__
    )
    while True:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=[{"role": "user", "content": prompt}],
                functions=functions,
                function_call={"name": "navigation"},
                request_timeout=2,
            )
            data = json.loads(
                response["choices"][0]["message"]["function_call"]["arguments"]
            )
            type = data["type"]
            if type == "data":
                return "visualizeData()"
            elif type == "track":
                return "visualizeTrack()"
            elif type == "visitor":
                return "visualizeVisitor()"
            else:
                raise HTTPException(status_code=500, detail="无法识别的页面类型")
            break
        except Timeout:
            retry_count += 1
            if retry_count > max_retries:
                raise HTTPException(
                    status_code=504,
                    detail=timeout_log_message,
                )
            else:
                logger.warning(timeout_log_message)
                continue
