# coding:utf8
from app.auth.service import forward
from app.util.proto import system_pb2, login_pb2


def system_notice(dynamic_id, content):
    response = system_pb2.m_9001_toc()
    response.content = content
    forward.push_object(9001, response.SerializeToString(), [dynamic_id])


def account_register(dynamic_id, user_name, password, account_id):
    response = login_pb2.m_1001_toc()
    response.user_name = user_name
    response.password = password
    response.account_id = account_id
    forward.push_object(1001, response.SerializeToString(), [dynamic_id])


def account_verify_official(dynamic_id, t, account_id, verify_key):
    response = login_pb2.m_1002_toc()
    response.time = t
    response.account_id = account_id
    response.verify_key = verify_key
    forward.push_object(1002, response.SerializeToString(), [dynamic_id])


def account_verify_channel(dynamic_id, t, account_id, verify_key):
    response = login_pb2.m_1002_toc()
    response.time = t
    response.account_id = account_id
    response.verify_key = verify_key
    forward.push_object(1003, response.SerializeToString(), [dynamic_id])





