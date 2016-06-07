# coding:utf8

import json
import os
import sys
import affinity
import signal
from twisted.python import log
from twisted.python.logfile import DailyLogFile
from twisted.internet import reactor
from twisted.web import vhost
from firefly.distributed.root import PBRoot, BilateralFactory
from firefly.distributed.node import RemoteObject
from firefly.dbentrust.memclient import mclient
from firefly.netconnect.protoc import LiberateFactory
from firefly.server.server import FFServer
from firefly.server.globalobject import GlobalObject
from firefly.utils import services
from firefly.web.delayrequest import DelaySite
from app.util.common import func
from app.util.driver.dbexecute import db_pool


if os.name != 'nt' and os.name != 'posix':
    from twisted.internet import epollreactor
    epollreactor.install()


class FFGServer(FFServer):

    def config(self, config, servername=None, dbconfig=None, memconfig=None, masterconf=None):
        GlobalObject().json_config = config
        netport = config.get('netport')         # 客户端连接
        webport = config.get('webport')         # http连接
        rootport = config.get('rootport')       # root节点配置
        self.remoteportlist = config.get('remoteport', [])   # remote节点配置列表
        if not servername:
            servername = config.get('name')     # 服务器名称
        logpath = config.get('log')             # 日志
        hasdb = config.get('db')                # 数据库连接
        hasmem = config.get('mem')              # memcached连接
        app = config.get('app')                 # 入口模块名称
        cpuid = config.get('cpu')               # 绑定cpu
        mreload = config.get('reload')          # 重新加载模块名称
        self.servername = servername
        if masterconf:
            masterport = masterconf.get('rootport')
            masterhost = masterconf.get('roothost')
            self.master_remote = RemoteObject(servername)
            addr = ('localhost',masterport) if not masterhost else (masterhost,masterport)
            self.master_remote.connect(addr)
            GlobalObject().masterremote = self.master_remote

        if netport:
            self.netfactory = LiberateFactory()
            netservice = services.CommandService("netservice")
            self.netfactory.addServiceChannel(netservice)
            reactor.listenTCP(netport,self.netfactory)

        if webport:
            self.webroot = vhost.NameVirtualHost()
            GlobalObject().webroot = self.webroot
            reactor.listenTCP(webport, DelaySite(self.webroot))

        if rootport:
            self.root = PBRoot()
            rootservice = services.Service("rootservice")
            self.root.addServiceChannel(rootservice)
            reactor.listenTCP(rootport, BilateralFactory(self.root))

        for cnf in self.remoteportlist:
            rname = cnf.get('rootname')
            self.remote[rname] = RemoteObject(self.servername)

        if hasdb and dbconfig:
            log.msg(str(dbconfig))
            db_pool.init_db_pool(**dbconfig)

        if hasmem and memconfig:
            urls = memconfig.get('urls')
            hostname = str(memconfig.get('hostname'))
            mclient.connect(urls, hostname)
        log_obj = DailyLogFile('master.log', 'logs/')
        log.FileLogObserver(log_obj)
        log.startLogging(sys.stdout)

        if cpuid:
            affinity.set_process_affinity_mask(os.getpid(), cpuid)
        GlobalObject().config(netfactory=self.netfactory, root=self.root,
                              remote=self.remote)
        if app:
            __import__(app)
        if mreload:
            _path_list = mreload.split(".")
            GlobalObject().reloadmodule = __import__(mreload, fromlist=_path_list[:1])
        GlobalObject().remote_connect = self.remote_connect
        import firefly.server.admin

    def start_after(self):
        func.log_info('{} has started, the pid is {}.'.format(self.servername, os.getpid()))

    def stop_before(self):
        func.log_info('{} is stoped.'.format(self.servername))
        if GlobalObject().stophandler:
            GlobalObject().stophandler()
        signal.alarm(1)

    def start(self):
        reactor.addSystemEventTrigger('after', 'startup', self.start_after)
        reactor.addSystemEventTrigger('before', 'shutdown', self.stop_before)
        GlobalObject().server = self
        FFServer.start(self)


if __name__ == "__main__":
    args = sys.argv
    server_name = None
    config = None
    if len(args) > 2:
        server_name = args[1]
        config = json.load(open(args[2], 'r'))
    else:
        raise ValueError
    dbconf = config.get('db')
    memconf = config.get('memcached')
    sersconf = config.get('servers', {})
    masterconf = config.get('master', {})
    serconfig = sersconf.get(server_name)
    ser = FFGServer()
    ser.config(serconfig, servername=server_name, dbconfig=dbconf, memconfig=memconf, masterconf=masterconf)
    ser.start()
