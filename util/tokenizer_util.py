import tiktoken
from typing import List


def get_num_tokens(model: str, text: str) -> List[int]:
    enc = tiktoken.encoding_for_model(model)
    tokenized_text = enc.encode(text)
    return len(tokenized_text)
