# coding:utf8
from twisted.web import resource
from firefly.server.globalobject import GlobalObject
from app.gate.action import infomation
from app.util.common import func


root = GlobalObject().webroot


def webapp_handle(cls):
    root.putChild(cls.__name__, cls())


@webapp_handle
class Information(resource.Resource):

    def render(self, request):
        # info_id = request.args
        # TODO: Information
        print 'Alex args: ', request.args
        info_id = int(request.args.get('id')[0])
        func.log_info('[gate] Infomation info_id: {}'.format(info_id))
        infomation.information_execute(info_id)
        return "success"
