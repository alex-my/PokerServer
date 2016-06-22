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
    管理后台对infomation表的操作 http://127.0.0.1:11861/Information?id=1
    """
    def render(self, request):
        info_id = int(request.args.get('id')[0])
        func.log_info('[gate] Infomation info_id: {}'.format(info_id))
        infomation.information_execute(info_id)
        return "SUCCESS"


@webapp_handle
class ServerInformation(resource.Resource):
    """
    输出服务器信息  http://127.0.0.1:11861/ServerInformation
    """
    def render(self, request):
        func.log_info('[gate] ServerInfomation')
        info = infomation.output_server_information()
        return info


@webapp_handle
class RechargeWechatNotify(resource.Resource):
    """
    微信充值成功的异步通知
    """
    isLeaf = True

    def render(self, request):
        try:
            recharge.wechat_recharge_success(request.content.read())
        except Exception as e:
            func.log_error('[gate] RechargeWechatNotify error: {}'.format(e.message))
        return "SUCCESS"


@webapp_handle
class RechargeWechatTest(resource.Resource):
    """
    测试充值 http://127.0.0.1:11861/RechargeWechatTest
    """
    def render(self, request):
        recharge.test_wechat_prepay_id(1, '12345')
        return "SUCCESS"


@webapp_handle
class AwardGold(resource.Resource):
    """
    直接充值金币
    120.76.153.160:11861/AwardGold?id=X&&gold=Y
    127.0.0.1:11861/AwardGold?id=X&&gold=Y
    """
    def render(self, request):
        role_id = int(request.args.get('id')[0])
        gold_count = int(request.args.get('gold')[0])
        return infomation.gm_award_gold(role_id, gold_count)


@webapp_handle
class ModifyAccountId(resource.Resource):
    """
    强制更改账号ID
    120.76.153.160:11861/ModifyAccountId?id=380001&&id=388888
    http://127.0.0.1:11861/ModifyAccountId?id=380001&&id=388888
    """
    def render(self, request):
        old_account_id = int(request.args.get('id')[0])
        cur_account_id = int(request.args.get('id')[1])
        func.log_info('[gate] ModifyAccountId old_account_id: {}, cur_account_id: {}'.format(
            old_account_id, cur_account_id
        ))
        return infomation.modify_account_id(old_account_id, cur_account_id)
