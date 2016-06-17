#!/usr/bin/env python
# coding:utf8
"""
客户端模拟器
"""
import os
import sys
from twisted.internet import reactor, protocol
from firefly.utils.singleton import Singleton
from firefly.utils.services import CommandService

reload(sys)
sys.setdefaultencoding("utf-8")

# 将上一级目录添加到环境变量中
path = os.path.dirname(os.getcwd())
sys.path.append(path)

from app.util.common import protocol as client_protocol
from app.util.common import func
from app.util.defines import operators, channel, rule
from app.util.proto import login_pb2, system_pb2, room_pb2, play_pb2, game_poker_pb2, game_mahjong_pb2

reactor = reactor


if os.name != 'nt' and os.name != 'posix':
    from twisted.internet import epollreactor
    epollreactor.install()


client_config = {
    'auth_server_ip': '120.76.153.160',
    # 'auth_server_ip': '127.0.0.1',
    'auth_server_port': 12831,
    'user_name': 'test1',
    'password': '1'
}


def deferred_error_handle(e):
    """
    延迟对象的错误处理
    :param e:
    :return:
    """
    func.log_error(str(e))
    return


class ClientProtocol(protocol.Protocol):

    def __init__(self, factory):
        self._factory = factory
        self._data_handler = self.data_handle_coroutine()
        self._buffer = ''

    def connectionMade(self):
        func.log_info('[ClientProtocol] connection made')
        self._factory.do_connect_made(self)
        self._data_handler.next()

    def connectionLost(self, reason=protocol.connectionDone):
        func.log_info('[ClientProtocol] connection lost')
        self._factory.clientConnectionLost(self, 'connectionLost')

    def dataReceived(self, data):
        self._buffer += data
        length = self._factory.data_protocol.getHeadlength()       # 获取协议头的长度
        while self._buffer.__len__() >= length:
            un_pack_data = self._factory.unpack(self._buffer[:length])
            if not un_pack_data.get('result'):
                # 数据异常, 断开重连
                func.log_info('illegal data package --')
                self.transport.loseConnection()
                break
            command = un_pack_data.get('command')
            rlength = un_pack_data.get('length')
            request = self._buffer[length:length+rlength]
            if request.__len__() < rlength:
                func.log_info('Data is not complete, waiting for the data ...')
                break
            self._buffer = self._buffer[length+rlength:]
            key, d = self._factory.do_data_received(command, request)
            if not d:
                continue
            d.addCallback(self.safeToWriteData, command, key)
            d.addErrback(deferred_error_handle)

    def safeToWriteData(self, data, command, key=None):
        if not self.transport.connected or data is None:
            return
        send_data = self._factory.pack(command, data)
        reactor.callFromThread(self.transport.write, send_data)

    def data_handle_coroutine(self):
        length = self._factory.data_protocol.getHeadlength()       # 获取协议头的长度
        while True:
            data = yield
            self._buffer += data
            while self._buffer.__len__() >= length:
                un_pack_data = self._factory.dataProtocol.unpack(self._buffer[:length])
                if not un_pack_data.get('result'):
                    # 数据异常, 断开重连
                    func.log_info('illegal data package --')
                    self.transport.loseConnection()
                    break
                command = un_pack_data.get('command')
                rlength = un_pack_data.get('length')
                request = self._buffer[length:length + rlength]
                if request.__len__() < rlength:
                    func.log_info('Data is not complete, waiting for the data ...')
                    break
                self._buffer = self._buffer[length + rlength:]
                key, d = self._factory.do_data_received(command, request)
                if not d:
                    continue
                d.addCallback(self.safeToWriteData, command, key)
                d.addErrback(deferred_error_handle)


class ClientFactory(protocol.ClientFactory):

    def __init__(self):
        self._client = None
        self._service = None
        self._data_protocol = None

    @property
    def data_protocol(self):
        return self._data_protocol

    def pack(self, command, data):
        return self._data_protocol.pack(data, command)

    def unpack(self, bytes):
        return self._data_protocol.unpack(bytes)

    def set_client(self, client, data_protocol):
        self._client = client
        self._service = client.service
        self._data_protocol = data_protocol

    def buildProtocol(self, addr):
        func.log_info('[ClientFactory] connected')
        return ClientProtocol(self)

    def startedConnecting(self, connector):
        func.log_info('[ClientFactory] start connect')

    def do_connect_made(self, conn):
        func.log_info('[ClientFactory] connect made: {}'.format(conn))
        self._client.conn = conn
        # 成功连接账号服务器
        if self._client.auth_node:
            # 裸包注册账号
            register_account(self._client, self._client.user_name, self._client.password)
            # 裸包登陆
            # account_verify_official(self._client, self._client.user_name, self._client.password)
            # 渠道登陆
            # account_verify_channel(self._client, self._client.user_name)
        # 成功连接游戏服务器
        else:
            user_login(self._client)

    def do_data_received(self, target_key, request):
        if client_service.is_target_local(target_key):
            result = client_service.callTarget(target_key, request)
            return target_key, result
        else:
            func.log_error('[ClientFactory] target_key: {} can not find in client_service'.format(target_key))
            return None, None

    def clientConnectionLost(self, connector, reason):
        func.log_info('[ClientFactory] connect lost, error: {}'.format(reason))

    def clientConnectionFailed(self, connector, reason):
        func.log_info('[ClientFactory] connect failed, error: {}'.format(reason))


class ClientCommandService(CommandService):

    def is_target_local(self, target_key):
        return target_key in self._targets

client_service = ClientCommandService('ClientService')
data_pack_proto = client_protocol.DataPackProto()  # 协议头


def client_service_handle(target):
    client_service.mapTarget(target)


class Client:

    __metaclass__ = Singleton

    def __init__(self):
        self._user_name = None
        self._password = None
        self._verify_key = None
        self._server_t = None
        self._account_id = None
        self._gold = None
        self._point = None
        self._service = None
        self._conn = None
        self._auth_node = True
        self._last_room_id = 0
        self._last_room_type = 0
        self._room_data = {}
        self.init()

    def init(self):
        self._load_config()
        self._service = client_service

    def _load_config(self):
        self._user_name = client_config['user_name']
        self._password = client_config['password']

    @property
    def user_name(self):
        return self._user_name

    @user_name.setter
    def user_name(self, name):
        self._user_name = name

    @property
    def password(self):
        return self._password

    @property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, _id):
        self._account_id = _id

    @property
    def auth_node(self):
        return self._auth_node

    @auth_node.setter
    def auth_node(self, state):
        self._auth_node = state

    @property
    def verify_key(self):
        return self._verify_key

    @verify_key.setter
    def verify_key(self, key):
        self._verify_key = key

    @property
    def service(self):
        return self._service

    @property
    def gold(self):
        return self._gold

    @gold.setter
    def gold(self, _gold):
        self._gold = _gold

    @property
    def point(self):
        return self._point

    @point.setter
    def point(self, _point):
        self._point = _point

    @property
    def room_data(self):
        return self._room_data

    @room_data.setter
    def room_data(self, data):
        self._room_data = data

    def add_last_room(self, room_id, room_type):
        self._last_room_id = room_id
        self._last_room_type = room_type

    @property
    def server_t(self):
        return self._server_t

    @server_t.setter
    def server_t(self, t):
        self._server_t = t

    @property
    def conn(self):
        return self._conn

    @conn.setter
    def conn(self, _conn):
        self._conn = _conn

    def connect_to_auth(self):
        self._connect(client_config['auth_server_ip'], client_config['auth_server_port'])

    def connect_to_game(self, ip, port):
        if ip and port:
            self._connect(ip, port)
        else:
            func.log_error('[Client] connect_to_game ip and port can not be null')

    def _connect(self, ip, port):
        func.log_info('[Client] _connect, ip: {}, port: {}'.format(ip, port))
        factory = ClientFactory()
        factory.set_client(self, data_pack_proto)
        reactor.connectTCP(ip, port, factory)

    def push_object(self, target_key, msg):
        if self._conn:
            self._conn.safeToWriteData(msg, target_key)

    def display_user(self):
        func.log_info('account_id: {}'.format(self._account_id))
        func.log_info('gold: {}, point: {}'.format(self._gold, self._point))
        func.log_info('last_room_id: {}, last_room_type: {}'.format(
            self._last_room_id, self._last_room_type
        ))


# 1001  账号注册
def register_account(client, user_name, password):
    func.log_info('[register_account] user_name: {}, password: {}'.format(user_name, password))
    response = login_pb2.m_1001_tos()
    response.user_name = user_name
    response.password = password
    client.push_object(1001, response.SerializeToString())


@client_service_handle
def register_account_1001(request):
    argument = login_pb2.m_1001_toc()
    argument.ParseFromString(request)
    client = Client()
    client.account_id = argument.account_id
    func.log_info('[register_account_1001] account_id: {}'.format(client.account_id))
    return None


# 1002 裸包账号登陆
def account_verify_official(client, user_name, password):
    func.log_info('[account_verify] user_name: {}, password: {}'.format(user_name, password))
    response = login_pb2.m_1002_tos()
    response.user_name = user_name
    response.password = password
    client.push_object(1002, response.SerializeToString())


@client_service_handle
def account_verify_1002(request):
    argument = login_pb2.m_1002_toc()
    argument.ParseFromString(request)
    client = Client()
    client.server_t = argument.time
    client.account_id = argument.account_id
    client.verify_key = argument.verify_key
    func.log_info('[account_verify_1002] account_id: {}, verify_key: {}, server_t: {}'.format(
        client.account_id, client.verify_key, client.server_t
    ))
    user_login(client)
    return None


# 1003 渠道账号登陆
def account_verify_channel(client, user_name):
    func.log_info('[account_verify] user_name: {}'.format(user_name))
    response = login_pb2.m_1003_tos()
    response.user_name = user_name
    response.channel_id = channel.CHANNEL_WE_CHAT
    response.uuid = user_name
    response.name = user_name
    response.head_frame = '123'
    response.head_icon = '345'
    response.sex = 1
    client.push_object(1003, response.SerializeToString())


@client_service_handle
def account_verify_1003(request):
    argument = login_pb2.m_1002_toc()
    argument.ParseFromString(request)
    client = Client()
    client.server_t = argument.time
    client.account_id = argument.account_id
    client.verify_key = argument.verify_key
    func.log_info('[account_verify_1003] account_id: {}, verify_key: {}, server_t: {}'.format(
            client.account_id, client.verify_key, client.server_t
    ))
    user_login(client)
    return None


# 账号登陆 2001
def user_login(client):
    func.log_info('[user_login] user_id: {} login begin'.format(client.account_id))
    response = login_pb2.m_2001_tos()
    response.account_id = client.account_id
    response.verify_key = client.verify_key
    client.push_object(2001, response.SerializeToString())


@client_service_handle
def user_login_2001(request):
    argument = login_pb2.m_2001_toc()
    argument.ParseFromString(request)
    client = Client()
    # user info
    client.account_id = argument.user_info.account_id
    client.uuid = argument.user_info.uuid
    client.user_name = argument.user_info.name
    client.gold = argument.user_info.gold
    client.point = argument.user_info.point
    client.add_last_room(argument.user_info.room_id, argument.user_info.room_type)
    # room info
    room_data = dict()
    for room_info in argument.room_info:
        prices = dict()
        for room_price in room_info.room_price:
            prices[room_price.rounds] = room_price.gold_price
        room_data[room_info.room_type] = {
            'room_id': room_info.room_id,
            'price': prices
        }
    client.room_data = room_data
    func.log_info('[user_enter_2002]')
    client.display_user()
    # ================ test create room
    # create_room(client, rule.GAME_TYPE_PDK2, 10)
    # ================ test enter room
    enter_room(client, 503327)
    return None


# 创建房间
def create_room(client, room_type, rounds):
    func.log_info('[create_room] room_type: {}'.format(room_type))
    response = room_pb2.m_3001_tos()
    response.room_type = room_type
    response.rounds = rounds
    client.push_object(3001, response.SerializeToString())


@client_service_handle
def create_room_3001(request):
    argument = room_pb2.m_3001_toc()
    argument.ParseFromString(request)
    client = Client()

    func.log_info('[create_room_3001] room_id: {}, room_type: {}, rounds: {}'.format(
        argument.room_id, argument.room_type, argument.rounds
    ))
    # enter room
    enter_room(client, argument.room_id)
    return None


def enter_room(client, room_id):
    func.log_info('[enter_room] room_id: {}'.format(room_id))
    response = room_pb2.m_3002_tos()
    response.room_id = room_id
    client.push_object(3002, response.SerializeToString())


@client_service_handle
def enter_room_3002(request):
    argument = room_pb2.m_3002_toc()
    argument.ParseFromString(request)
    client = Client()
    func.log_info('[enter_room_3002] room_id: {}, user_id: {}, rounds: {}, max_rounds: {}'.format(
            argument.room_id, argument.user_id, argument.rounds, argument.max_rounds))
    # 准备
    user_ready(client)


@client_service_handle
def enter_room_3003(request):
    argument = room_pb2.m_3003_toc()
    argument.ParseFromString(request)
    client = Client()
    func.log_info('[enter_room_3003] room_id: {}, user_id: {}, rounds: {}, max_rounds: {}'.format(
            argument.room_id, argument.user_id, argument.rounds, argument.max_rounds))
    func.log_info('mahjong ---- maker_account_id: {}, craps: {}, mahjong_start_num: {}, mahjong_end_num: {}'.format(
        argument.maker_account_id, [craps_id for craps_id in argument.craps],
        argument.mahjong_start_num, argument.mahjong_end_num
    ))
    # 准备
    user_ready(client)


def user_ready(client):
    func.log_info('[user_ready]')
    response = play_pb2.m_4001_toc()
    response.operate = operators.USER_OPERATOR_READY
    client.push_object(4001, response.SerializeToString())


@client_service_handle
def user_ready_4001(request):
    argument = play_pb2.m_4001_toc()
    argument.ParseFromString(request)
    client = Client()
    func.log_info('[user_ready_4001] operate: {}'.format(argument.operate))


@client_service_handle
def user_dispatch_card_4002(request):
    argument = play_pb2.m_4002_toc()
    argument.ParseFromString(request)
    client = Client()
    func.log_info('[user_publish_card_4002] account_id: {}, operate: {}'.format(
        argument.account_id, argument.operate))


@client_service_handle
def user_publish_card_4003(request):
    argument = play_pb2.m_4003_toc()
    argument.ParseFromString(request)
    client = Client()
    card_list = [card_id for card_id in argument.cards]
    func.log_info('[user_publish_card_4003] execute_account_id: {}, card_list: {}'.format(
        argument.execute_account_id, card_list
    ))
    # poker_publish(client, card_list)
    # mahjong_publish(client, card_list[0])


def poker_publish(client, card_list):
    response = game_poker_pb2.m_5101_tos()
    response.cards.append(card_list[0])
    func.log_info('[poker_publish] card_id: {}'.format(card_list[0]))
    client.push_object(5101, response.SerializeToString())


@client_service_handle
def poker_publish_5101(request):
    func.log_info('[poker_publish_5101]')


@client_service_handle
def poker_publish_all_5102(request):
    argument = game_poker_pb2.m_5102_toc()
    argument.ParseFromString(request)
    client = Client()
    card_list = [card_id for card_id in argument.cards]
    func.log_info('[poker_publish_all_5102] execute_account_id: {}, next_account_id: {}, cards: {}'.format(
        argument.execute_account_id, argument.next_account_id, card_list
    ))


@client_service_handle
def mahjong_publish_5201(request):
    argument = game_mahjong_pb2.m_5201_toc()
    argument.ParseFromString(request)
    client = Client()
    craps_list = [craps_id for craps_id in argument.craps]
    func.log_info('[mahjong_publish_5201] maker_account_id: {}, craps: {}, mahjong_start_num: {}, mahjong_end_num: {}'.format(
        argument.maker_account_id, craps_list, argument.mahjong_start_num, argument.mahjong_end_num
    ))


@client_service_handle
def mahjong_dispatch_5202(request):
    argument = game_mahjong_pb2.m_5202_toc()
    argument.ParseFromString(request)
    operator_list = [operator_id for operator_id in argument.operator]
    func.log_info('[mahjong_dispatch_5202] card: {}, operator: {}'.format(argument.card, operator_list))


def mahjong_publish(client, card_id):
    response = game_mahjong_pb2.m_5203_tos()
    response.card = card_id
    func.log_info('[mahjong_publish] card_id: {}'.format(card_id))
    client.push_object(5203, response.SerializeToString())


@client_service_handle
def mahjong_publish_5203(request):
    func.log_info('[mahjong_publish_5203]')


@client_service_handle
def mahjong_publish_5204(request):
    argument = game_mahjong_pb2.m_5204_toc()
    argument.ParseFromString(request)
    operator_list = [operator for operator in argument.operator]
    card_list = [card_id for card_id in argument.card_list]
    func.log_info('[mahjong_publish_5204] execute_account_id: {}, card: {}, card_list: {}, operator_able: {}, operator_list: {}'.format(
        argument.execute_account_id, argument.card, card_list, argument.operator_able, operator_list
    ))


# 9001 系统消息
@client_service_handle
def system_notice_9001(request):
    argument = system_pb2.m_9001_toc()
    argument.ParseFromString(request)
    func.log_error('[SYSTEM] {}'.format(argument.content))
    return None


@client_service_handle
def user_change_9003(request):
    argument = system_pb2.m_9003_toc()
    argument.ParseFromString(request)
    change_list = [c for c in argument.role_change]
    role_change_list = [{'change_type': info.change_type, 'change_value': info.change_value} for info in change_list]
    func.log_info('[user_change_9003] role_change_list: {}'.format(role_change_list))
    return None


# 9004 走马灯
@client_service_handle
def system_notice_9004(request):
    pass


if __name__ == '__main__':
    Client().connect_to_auth()
    reactor.run()
