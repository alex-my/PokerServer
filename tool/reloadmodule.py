#!/usr/bin/env python
# coding:utf8

import urllib

url = "http://%s:%s/reloadmodule" % ('127.0.0.1', 11821)
urllib.urlopen(url)
