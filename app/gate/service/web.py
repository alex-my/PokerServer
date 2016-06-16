# coding:utf8
from twisted.web import resource
from firefly.server.globalobject import GlobalObject
from app.gate.action import infomation, recharge
from app.util.common import func


root = GlobalObject().webroot


def webapp_handle(cls):
    root.putChild(cls.__name__, cls())


@webapp_handle
class Information(resource.Resource):
    """
    管理后台对infomation表的操作
    """
    def render(self, request):
        info_id = int(request.args.get('id')[0])
        func.log_info('[gate] Infomation info_id: {}'.format(info_id))
        infomation.information_execute(info_id)
        return "SUCCESS"


@webapp_handle
class RechargeWechatNotify(resource.Resource):
    """
    微信充值成功的异步通知
    """
    def render(self, request):
        # TODO: RechargeWechatNotify GET
        print 'RechargeNotify render request: ', request.args
        return "SUCCESS"

    def render_POST(self, request):
        # TODO: RechargeWechatNotify POST
        print 'RechargeNotify render_POST request: ', request.args
        return "SUCCESS"


@webapp_handle
class RechargeWechatTest(resource.Resource):
    """
    测试充值 http://127.0.0.1:8621/RechargeWechatTest
    """
    def render(self, request):
        recharge.test_wechat_prepay_id(1, '12345')
        return "SUCCESS"


