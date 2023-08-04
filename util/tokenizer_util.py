import tiktoken


def get_num_tokens(model: str, text: str) -> list[int]:
    enc = tiktoken.encoding_for_model(model)
    tokenized_text = enc.encode(text)
    return len(tokenized_text)
