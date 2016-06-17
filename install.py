#!/usr/bin/env python
# coding:utf8
import os
import sys
import codecs
import subprocess


SERVICE_NAME = "bbg"
SERVICE_PORT = "11821"


def args_help():
    print "usage: python install.py [args]"
    print "Valid args:"
    print "  install                        : Install service"
    print "  uninstall                      : Uninstall service"


def install(service_name):
    path = os.path.split(os.path.realpath(__file__))[0]
    output = codecs.open("/etc/init.d/%s" % service_name, "w", 'utf-8')
    output.write(build_service_script(service_name, path, SERVICE_PORT))
    output.close()
    subprocess.call(["chmod +x /etc/init.d/%s" % service_name], shell=True, stdout=subprocess.PIPE)
    print "%s service installed!" % service_name


def uninstall(service_name):
    subprocess.call(["rm /etc/init.d/%s" % service_name], shell=True, stdout=subprocess.PIPE)
    print "%s service uninstalled!" % service_name


def build_service_script(service_name, path, port):
    """
    构建服务脚本
    """
    return """
#!/bin/bash

export PATH="""+ os.environ.get("PATH") +"""

start() {
    cd """ + path + """
    python startmaster.py >> logs/master.log &
    echo "Starting """ + service_name + """ server ..."
}

stop() {
    curl http://127.0.0.1:""" + port + """/stop
    echo "Stoping """ + service_name + """ server ..."
}

reload() {
    curl http://127.0.0.1:""" + port + """/reloadmodule
    echo "Reloading """ + service_name + """ server ..."
}

version() {
    cd """ + path + """ && svn info
}

update() {
    cd """ + path + """ && git pull origin master
}

status() {
    echo "server """ + service_name + """ status :"
    curl http://127.0.0.1:""" + port + """/status
}

status2() {
    cd """ + path + """ && python status.py `cat twistd.pid`
}

master() {
    tail -f """ + path + """/logs/master.log
}

case "$1" in
    start)
start
;;
    stop)
stop
;;
    reload)
reload
;;
    version)
version
;;
    update)
update
;;
    status)
status
;;
    status2)
status2
;;
    master)
master
;;
    *)
echo $"Usage $0 {start|stop|reload|backup|version|update|status|master}"
exit 2
esac
    """

if __name__ == "__main__":
    args = sys.argv[1:]
    if not len(args):
        args_help()
    command = args[0]
    if len(args) > 1:
        service = args[1]
    else:
        service = SERVICE_NAME
    if command in ['remove', 'uninstall']:
        uninstall(service)
    elif command == "install":
        install(service)
    else:
        args_help()
