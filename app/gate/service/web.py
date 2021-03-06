# coding:utf8
from twisted.web import resource
from firefly.server.globalobject import GlobalObject
from app.gate.action import infomation, recharge, login
from app.util.common import func


root = GlobalObject().webroot


def webapp_handle(cls):
    root.putChild(cls.__name__, cls())


@webapp_handle
class Information(resource.Resource):
    """
    127.0.0.1:11861/Information?id=1
    """
    def render(self, request):
        info_id = int(request.args.get('id')[0])
        func.log_info('[gate] Infomation info_id: {}'.format(info_id))
        infomation.information_execute(info_id)
        return "SUCCESS"


@webapp_handle
class ServerInformation(resource.Resource):
    """
    120.76.153.160:11861/ServerInformation
    """
    def render(self, request):
        func.log_info('[gate] ServerInfomation')
        info = infomation.output_server_information()
        return info


@webapp_handle
class RechargeWechatNotify(resource.Resource):

    isLeaf = True

    def render(self, request):
        try:
            recharge.wechat_recharge_success(request.content.read())
        except Exception as e:
            func.log_error('[gate] RechargeWechatNotify error: {}'.format(e.message))
        return "SUCCESS"


@webapp_handle
class RechargeStasticsTest(resource.Resource):
    """
    120.76.153.160:11861/RechargeStasticsTest?id=380001
    127.0.0.1:11861/RechargeStasticsTest?id=380001
    """
    def render(self, request):
        try:
            account_id = int(request.args.get('id')[0])
            recharge.test_recharge_statistic(account_id)
        except Exception as e:
            func.log_error('[gate] RechargeStasticsTest error: {}'.format(e.message))
        return "SUCCESS"


@webapp_handle
class BindStasticsTest(resource.Resource):
    """
    120.76.153.160:11861/BindStasticsTest?id=380001
    127.0.0.1:11861/BindStasticsTest?id=380001
    """
    def render(self, request):
        try:
            account_id = int(request.args.get('id')[0])
            login.proxy_stastics(account_id)
        except Exception as e:
            func.log_error('[gate] RechargeStasticsTest error: {}'.format(e.message))
        return "SUCCESS"


@webapp_handle
class AwardGold(resource.Resource):
    """
    120.76.153.160:11861/AwardGold?id=X&&gold=Y
    127.0.0.1:11861/AwardGold?id=X&&gold=Y
    """
    def render(self, request):
        account_id = int(request.args.get('id')[0])
        gold_count = int(request.args.get('gold')[0])
        return recharge.gm_award_gold(account_id, gold_count)


@webapp_handle
class ModifyAccountId(resource.Resource):
    """
    120.76.153.160:11861/ModifyAccountId?id=380001&&id=388888
    127.0.0.1:11861/ModifyAccountId?id=380001&&id=388888
    """
    def render(self, request):
        old_account_id = int(request.args.get('id')[0])
        cur_account_id = int(request.args.get('id')[1])
        func.log_info('[gate] ModifyAccountId old_account_id: {}, cur_account_id: {}'.format(
            old_account_id, cur_account_id
        ))
        return infomation.modify_account_id(old_account_id, cur_account_id)


@webapp_handle
class IsUserOnline(resource.Resource):
    """
    120.76.153.160:11861/IsUserOnline?id=380001
    127.0.0.1:11861/IsUserOnline?id=380001
    """
    def render(self, request):
        account_id = int(request.args.get('id')[0])
        return login.is_user_online(account_id)


@webapp_handle
class SyncAllRechargeStatistic(resource.Resource):
    """
    120.76.153.160:11861/SyncAllRechargeStatistic
    127.0.0.1:11861/SyncAllRechargeStatistic
    """
    def render(self, request):
        func.log_info('[gate] SyncAllRechargeStatistic')
        recharge.sync_all_recharge_statistic()
        return "SUCCESS"


@webapp_handle
class SyncAllRechargeStatistic(resource.Resource):
    """
    120.76.153.160:11861/SyncAllRechargeStatistic
    127.0.0.1:11861/SyncAllRechargeStatistic
    """
    def render(self, request):
        func.log_info('[gate] SyncAllRechargeStatistic')
        recharge.sync_all_recharge_statistic()
        return "SUCCESS"


@webapp_handle
class SyncAllProxyCountStatistic(resource.Resource):
    """
    120.76.153.160:11861/SyncAllProxyCountStatistic
    127.0.0.1:11861/SyncAllProxyCountStatistic
    """
    def render(self, request):
        func.log_info('[gate] SyncAllProxyCountStatistic')
        login.sync_all_proxy_count_statistic()
        return "SUCCESS"


@webapp_handle
class SyncAllProxyRecharge(resource.Resource):
    """
    120.76.153.160:11861/SyncAllProxyRecharge
    127.0.0.1:11861/SyncAllProxyRecharge
    """
    def render(self, request):
        func.log_info('[gate] SyncAllProxyRecharge')
        recharge.sync_all_proxy_recharge()
        return "SUCCESS"


@webapp_handle
class SyncAllCommand(resource.Resource):
    """
    120.76.153.160:11861/SyncAllCommand
    127.0.0.1:11861/SyncAllCommand
    """
    def render(self, request):
        func.log_info('[gate] SyncAllCommand')
        recharge.sync_all_proxy_recharge()
        recharge.sync_all_recharge_statistic()
        login.sync_all_proxy_count_statistic()
        return "SUCCESS"


@webapp_handle
class RechargeFeeToYuan(resource.Resource):
    """
    120.76.153.160:11861/RechargeFeeToYuan
    127.0.0.1:11861/RechargeFeeToYuan
    """
    def render(self, request):
        func.log_info('[gate] RechargeFeeToYuan')
        recharge.recharge_fee_to_yuan()
        return "SUCCESS"

