from pydantic import BaseModel


class PaymentAlipayUrlRequest(BaseModel):
    username: str
    amount: float
    dev_mode: bool


class PaymentAlipayUrlResponse(BaseModel):
    url: str
