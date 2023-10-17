from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
# from alipay.aop.api.domain.SettleDetailInfo import SettleDetailInfo
# from alipay.aop.api.domain.SettleInfo import SettleInfo
# from alipay.aop.api.domain.SubMerchant import SubMerchant
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from baykeshop.pay.alipay.client import client


def trade_page_pay(
    out_trade_no='', total_amount=0, subject='', body='', 
    return_url=None, notify_url=None, client=client()
    ):
    """ 网页支付 """
    
    model = AlipayTradePagePayModel()
    model.out_trade_no = out_trade_no
    model.total_amount = total_amount
    model.subject = subject
    model.body = body
    model.product_code = "FAST_INSTANT_TRADE_PAY"
    
    # settle_detail_info = SettleDetailInfo()
    request = AlipayTradePagePayRequest(biz_model=model)
    request.return_url = return_url
    request.notify_url = notify_url
    return client.page_execute(request, http_method="GET")
