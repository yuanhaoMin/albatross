import json
import tiktoken
import time


def tokenize(model: str, text: str) -> list[int]:
    enc = tiktoken.encoding_for_model(model)
    tokenized_text = enc.encode(text)
    return tokenized_text


def tokenize_and_convert_to_json_string(model: str, text: str) -> str:
    tokenized_text = tokenize(model, text)
    return json.dumps(tokenized_text)


def detokenize(model: str, tokenized_text: list[int]) -> str:
    enc = tiktoken.encoding_for_model(model)
    text = enc.decode(tokenized_text)
    return text


def detokenize_json(model: str, tokenized_text_json: str) -> str:
    tokenized_text = json.loads(tokenized_text_json)
    return detokenize(model, tokenized_text)


# model_name = "gpt-3.5-turbo"
# input_text = "".join(["我" for _ in range(10)])
# start_time = time.time()
# tokenized_text = tokenize(model_name, input_text)
# end_time = time.time()
# print("Execution time:", end_time - start_time, "seconds")
