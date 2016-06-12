# coding:utf8
from firefly.server.globalobject import GlobalObject
from app.gate.core.RoomProxyManager import RoomProxyManager
from app.gate.core.UserManager import UserManager
from app.util.common.config import Config
from app.util.common import func


def do_when_stop():
    func.log_info('[gate] ---------------------------> node do_when_stop begin')
    for account_id, user in UserManager().get_all_users().items():
        try:
            if not user:
                continue
            user.user_save()
        except Exception as e:
            func.log_error('[gate] user save account_id: {}, error: {}, user_data: {}'.format(
                account_id, e.message, user.get_save_data()
            ))
    func.log_info('[gate] node do_when_stop end <-----------------------')


GlobalObject().stophandler = do_when_stop


def load_module():
    import gateservice
    import service
    import timer

    Config().load_configs()
    RoomProxyManager().load_all_room()
    RoomProxyManager().load_configs()
