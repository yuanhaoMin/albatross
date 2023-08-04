import logging
from configuration.payment_alipay import get_alipay_object
from constant.subscription_plan_enum import SubscriptionPlanEnum
from datetime import datetime, timedelta
from persistence import user_crud
from schema import payment_schema
from service import user_service
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


def alipay_generate_url(
    request: payment_schema.PaymentAlipayUrlRequest, db: Session
) -> payment_schema.PaymentAlipayUrlResponse:
    alipay = get_alipay_object(request.dev_mode)
    user = user_service.get_user_by_username(request.username, db)
    current_date_str = datetime.now().strftime("%Y%m%d%H%M%S")
    # 14 digits of current time + user id
    out_trade_no = current_date_str + str(user.id)
    res = alipay.api_alipay_trade_page_pay(
        out_trade_no=out_trade_no,  # 订单号
        total_amount=request.amount,  # 价格
        subject=user.username + "的订阅",  # 名称
        return_url="https://albatross21python.azurewebsites.net/payment/alipay/success",  # 支付成功后会跳转的页面
        notify_url="https://albatross21python.azurewebsites.net/payment/alipay/notify",  # 回调地址，支付成功后支付宝会向这个地址发送post请求
    )
    if request.dev_mode:
        gataway = "https://openapi-sandbox.dl.alipaydev.com/gateway.do?"
    else:
        gataway = "https://openapi.alipay.com/gateway.do?"
    url = gataway + res
    return payment_schema.PaymentAlipayUrlResponse(url=url)


def alipay_get_success_info(
    out_trade_no: str,
    total_amount: float,
    db: Session,
):
    user_id = out_trade_no[14:]
    user = user_crud.get_user_by_id(user_id, db)
    subscription_plan = SubscriptionPlanEnum.from_price(int(total_amount))
    subscription_end_time = user.subscription_end_time + timedelta(
        days=31 * subscription_plan.month
    )
    user_crud.update_user_subscription(
        id=user.id,
        access_bitmap=subscription_plan.access_bitmap,
        subscription_end_time=subscription_end_time,
        db=db,
    )
    logger.warning('用户"{}"支付宝支付{}元'.format(user.username, total_amount))
    return "http://bizcampgpt.com/chat"


def alipay_notify():
    logger.warning("支付宝-回调成功")
    return "回调成功"
