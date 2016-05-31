# coding:utf8
import struct
from firefly.netconnect.datapack import DataPackError
from app.util.common import func


class DataPackProto(object):

    def __init__(self):
        self._encrypt = 0

    def getHeadlength(self):
        return 7

    def unpack(self, bytes):
        try:
            length, _, command = struct.unpack('!Ibh', bytes)[:3]
        except DataPackError as e:
            func.log_info('[unpack] failed: {}'.format(e.message))
            return {'result': False, 'command': 0, 'length': 0}
        return {'result': True, 'command': command, 'length': length}

    def pack(self, response, command):
        if isinstance(response, dict):
            result = response.get("result", '')
        else:
            result = response
        length = len(result)
        data = struct.pack("!Ibh", length, self._encrypt, command)
        data = data + result
        return data


