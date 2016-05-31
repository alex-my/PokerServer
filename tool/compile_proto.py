#!/usr/bin/env python
# coding:utf8
"""
编译python中的proto文件,拷贝proto到share, robot(并编译)目录，并提交到SVN
"""

import os
import shutil


def get_file_list(path, file_type, absolute):
    path = str(path)
    if path[-1] != '/':
        path += '/'
    if absolute:
        return [path + f for f in os.listdir(path) if os.path.isfile(path + f) and os.path.splitext(f)[1] == file_type]
    return [f for f in os.listdir(path) if os.path.isfile(path + f) and os.path.splitext(f)[1] == file_type]


def rm_files(files):
    for f in files:
        os.remove(f)


def execute_protoc(files, src_path, out_path):
    if src_path[-1] != '/':
        src_path += '/'
    if out_path[-1] != '/':
        out_path += '/'
    for f in files:
        cmd = "protoc -I=%s --python_out=%s %s" % (src_path, out_path, f)
        print 'cmd: ', cmd
        os.system(cmd)


def protocol(path):
    if path[-1] != '/':
        path += '/'

    rm_file_list = get_file_list(path, '.pyc', True)
    rm_files(rm_file_list)

    proto_file_list = get_file_list(path + 'source/', '.proto', True)
    execute_protoc(proto_file_list, path + 'source/', path)


def copy_proto(src_list, dst):
    if not isinstance(src_list, list):
        print 'src_list must be list ...'
        return
    dst = str(dst)
    if dst[-1] != '/':
        dst += '/'
    for src in src_list:
        shutil.copy(src, dst)
    print 'copy %d file success ...' % (len(src_list))


def commit_proto(path, file_type='*.proto'):
    """
    提交到svn
    :param path:
    :param file_type:
    :return:
    """
    path = str(path)
    if path[-1] != '/':
        path += '/'
    os.chdir(path)
    os.system('svn add %s' % file_type)
    os.system('svn commit -m  \'modify proto file\'')


def commit_to_share(src_path, dst_path):
    """
    拷贝到share目录
    :param src_path:
    :param dst_path:
    :return:
    """
    if src_path[-1] != '/':
        src_path += '/'
    if dst_path[-1] != '/':
        dst_path += '/'

    file_list = get_file_list(src_path + 'source/', '.proto', True)
    rst_list = get_file_list(src_path + 'source/', '.rst', True)
    if rst_list:
        file_list.extend(rst_list)
    copy_proto(file_list, dst_path)
    commit_proto(dst_path, file_type='*.proto')
    if rst_list:
        commit_proto(dst_path, file_type='*.rst')


if __name__ == '__main__':
    origin_path = os.getcwd()
    path = os.path.dirname(os.getcwd())
    share_path = os.path.dirname(path)
    src_path = '{}/app/util/proto'.format(path)
    dst_share_path = '{}/share/proto'.format(share_path)

    print 'compile_proto, src_path: {}'.format(src_path)
    print 'compile_proto, dst_share_path: {}'.format(dst_share_path)

    protocol(src_path)
    os.chdir(origin_path)

    commit_to_share(src_path, dst_share_path)
    os.chdir(origin_path)
