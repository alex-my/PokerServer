# coding:utf8

import hashlib
import json
import requests
import xml2json
from xml.etree import ElementTree
from app.util.common import func
from app.util.defines import constant, content


class WechatPay(object):

    def __init__(self):
        self._params = dict()
        self._url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
        self._error = None

    def init(self, **kwargs):
        func.log_info('[game] WechatPay init kwargs: {}'.format(kwargs))
        self._params = {
            'appid': constant.WECHAT_APPID,
            'mch_id': constant.WECHAT_MCH_ID,
            'nonce_str': kwargs['nonce_str'],                   # 随机字符串，不长于32位
            'body': constant.WECHAT_BODY,                       # 商品或支付单简要描述
            'attach': kwargs['attach'],                         # 商家附加数据, 127位
            'out_trade_no': str(kwargs['order_id']),            # 唯一商户订单号, 32位, 字母+数字均可
            'total_fee': str(int(kwargs['total_fee'])),         # 订单总金额，单位为分
            'spbill_create_ip': kwargs['spbill_create_ip'],     # 用户端实际ip
            'trade_type': 'APP',                                # 支付类型
            'notify_url': constant.WECHAT_NOTIFY_URL,           # 接收微信支付异步通知回调地址
            'limit_pay': 'no_credit'                            # 不能使用信用卡支付
        }

    @staticmethod
    def key_value_url(value):
        """
        将键值对转为 key1=value1&key2=value2
        :param value:
        :return:
        """
        key_az = sorted(value.keys())
        pair_array = []
        print 'Alex value: ', value
        for k in key_az:
            print 'Alex k: ', k
            v = value.get(k, '').strip()
            v = v.encode('utf8')
            k = k.encode('utf8')
            pair_array.append('%s=%s' % (k, v))

        tmp = '&'.join(pair_array)
        return tmp

    def get_sign(self, params):
        kvurl = self.key_value_url(params)
        s = kvurl + '&key=' + constant.WECHAT_APIKEY
        sign = (hashlib.md5(s).hexdigest()).upper()
        params['sign'] = sign

    def get_req_xml(self):
        """拼接XML
        """
        self.get_sign(self._params)
        xml = "<xml>"
        for k, v in self._params.items():
            v = v.encode('utf8')
            k = k.encode('utf8')
            xml += '<' + k + '>' + v + '</' + k + '>'
        xml += "</xml>"
        return xml

    def calc_prepay_id(self):
        xml = self.get_req_xml()
        headers = {'Content-Type': 'application/xml'}
        r = requests.post(self._url, data=xml, headers=headers)
        print u'Alex r: {}'.format(r.text)
        re_xml = ElementTree.fromstring(r.text.encode('utf8'))
        print 'Alex re_xml: ', re_xml.getiterator('result_code')
        xml_status = re_xml.getiterator('result_code')[0].text
        func.log_info('[game] WechatPay query_prepay_id xml_status: {}'.format(xml_status))
        if xml_status != 'SUCCESS':
            self._error = content.RECHARGE_WECHAT_CONNECT_FAILED
            return
        prepay_id = re_xml.getiterator('prepay_id')[0].text

        self._params['prepay_id'] = prepay_id
        self._params['package'] = 'Sign=WXPay'
        self._params['timestamp'] = str(func.time_get())

    def get_prepay_id(self):
        return self._params.get('prepay_id', -1)

    def re_finall(self):
        """
        得到prepay_id后再次签名，然后返回给客户端
        :return:
        """
        self.calc_prepay_id()
        if self._error:
            return

        sign_again_params = {
            'appid': self._params['appid'],
            'noncestr': self._params['nonce_str'],
            'package': self._params['package'],
            'partnerid': self._params['mch_id'],
            'timestamp': self._params['timestamp'],
            'prepayid': self._params['prepay_id']
        }
        self.get_sign(sign_again_params)
        self._params['sign'] = sign_again_params['sign']

        # 移除其他不需要返回参数
        for i in self._params.keys():
            if i not in ['appid', 'mch_id', 'nonce_str', 'timestamp', 'sign', 'package', 'prepay_id']:
                self._params.pop(i)
        return self._params


class WechatResponse(WechatPay):
    """
    签名验证
    """
    def __init__(self, xml):
        """
        :param xml: 支付成功回调的XML
        """
        super(WechatResponse, self).__init__()
        self._xml = xml
        # options = optparse.Values({"pretty": False})
        self._xml_json = json.loads(xml2json.xml2json(self._xml))['xml']
        self._sign = self._xml_json.get('sign', '')

    def verify(self):
        """验证签名"""

        self._xml_json.pop('sign')
        self.get_sign(self._xml_json)
        if self._sign != self._xml_json['sign']:
            func.log_error('[game] WechatResponse xml_sign: {} != sgin: {}'.format(
                    self._xml_json['sign'], self._sign))
            return False
        return True


def generator_unique_order_id(money):
    t = func.time_get()
    return str(money * 3 - func.random_get(30000, t))


def query_prepay_id(money, proxy_id, ip=''):
    pay = WechatPay()
    pay.init(
        nonce_str=func.random_string_r(16, 30),
        attach=str(proxy_id),
        order_id=generator_unique_order_id(money),
        total_fee=money * 100,
        spbill_create_ip=ip
    )
    pay.re_finall()


if __name__ == '__main__':
    pass

