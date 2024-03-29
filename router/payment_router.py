from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from schema.payment_schema import PaymentAlipayUrlRequest, PaymentAlipayUrlResponse
from service import payment_service
from sqlalchemy.orm import Session
from util.db_util import get_db


router = APIRouter(
    prefix="/payment",
    tags=["payment"],
    responses={404: {"description": "Not found"}},
)


@router.post("/alipay/url", response_model=PaymentAlipayUrlResponse)
def alipay_generate_url(
    request: PaymentAlipayUrlRequest, db: Session = Depends(get_db)
) -> PaymentAlipayUrlResponse:
    return payment_service.alipay_generate_url(request, db)


@router.get("/alipay/success", response_class=RedirectResponse)
def alipay_get_success_info(
    out_trade_no: str,
    total_amount: float,
    db: Session = Depends(get_db),
):
    return payment_service.alipay_get_success_info(out_trade_no, total_amount, db)


@router.post("/alipay/notify")
def alipay_notify():
    return payment_service.alipay_notify()
