# coding:utf8
from firefly.server.globalobject import GlobalObject
from app.util.common import func


def do_when_stop():
    func.log_info('[auth] ---------------------------> node do_when_stop <-----------------------')


GlobalObject().stophandler = do_when_stop


def load_module():
    import authservice
    import service


