from alipay import AliPay
from alipay.utils import AliPayConfig


def get_alipay_object(dev_mode: bool):
    app_private_key_string = open(
        "./configuration/alipay_app_private_key_RSA2048.txt"
    ).read()
    alipay_public_key_string = open(
        "./configuration/alipay_public_key_RSA2048.txt"
    ).read()
    alipay = AliPay(
        appid="9021000122685934",
        # 默认回调 url
        app_notify_url=None,
        app_private_key_string=app_private_key_string,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",
        # 是否是支付宝测试环境(沙箱环境)，如果采用真是支付宝环境，配置False
        debug=dev_mode,
        # 输出调试数据
        verbose=dev_mode,
        # 请求超时时间
        config=AliPayConfig(timeout=15),
    )
    return alipay
