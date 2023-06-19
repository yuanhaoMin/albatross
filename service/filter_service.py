import json
import openai

openai.api_key = "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"
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
prompt = "法轮功"
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[{"role": "user", "content": prompt}],
    functions=functions,
    function_call="auto",
    timeout=3,
)
data = json.loads(response["choices"][0]["message"]["function_call"]["arguments"])
result_bool = bool(data["result"])
print(result_bool)
