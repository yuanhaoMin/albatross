from pydantic import BaseModel


class PaymentAlipayUrlRequest(BaseModel):
    username: str
    amount: float


class PaymentAlipayUrlResponse(BaseModel):
    url: str
