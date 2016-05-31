#!/usr/bin/env python
# coding:utf8

import urllib

url = "http://%s:%s/stop" % ('127.0.0.1', 8521)
urllib.urlopen(url)
