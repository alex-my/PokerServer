# coding:utf8
"""
game节点管理器
"""
from twisted.internet import reactor
from firefly.server.globalobject import GlobalObject
from firefly.utils.singleton import Singleton
from app.gate.core.Node import ServerNode
from app.util.common import func


class NodeManager:

    __metaclass__ = Singleton

    def __init__(self):
        self._nodes = dict()
        self.init_nodes(True)

    def init_nodes(self, delay):
        for node_name in GlobalObject().root.childsmanager._childs.keys():
            if 'game' in node_name:
                self._add_node(node_name)
        if delay:
            reactor.callLater(30, self.init_nodes, False)

    def _add_node(self, node_name):
        if node_name not in self._nodes:
            func.log_info('[NodeManager] node: {} join'.format(node_name))
            node = ServerNode(node_name)
            self._nodes[node_name] = node

    def get_node(self, node_name):
        return self._nodes.get(node_name)

    def get_all_nodes_list(self):
        return self._nodes.values()

    def get_node_user_count(self, node_name):
        node = self.get_node(node_name)
        if node:
            player_count = node.get_users_count()
        else:
            player_count = 0
        return player_count
