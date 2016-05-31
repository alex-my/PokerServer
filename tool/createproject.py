#!/usr/bin/env python
# coding:utf8
import sys
from firefly import management


if __name__ == '__main__':
    args = sys.argv
    management.execute_commands(*args)
