import tiktoken
from typing import List


def get_num_tokens(model: str, text: str) -> List[int]:
    enc = tiktoken.encoding_for_model(model)
    tokenized_text = enc.encode(text)
    return len(tokenized_text)


# model_name = "gpt-3.5-turbo"
# input_text = "".join(["我" for _ in range(10)])
# start_time = time.time()
# tokenized_text = tokenize(model_name, input_text)
# end_time = time.time()
# print("Execution time:", end_time - start_time, "seconds")
