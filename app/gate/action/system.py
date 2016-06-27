# coding:utf8
import datetime
import os
import stat
import time
import tarfile
from app.util.common import func
from app.util.defines import constant


def clear_logs():
    logs_path = os.getcwd() + '/logs/'
    clear_files(logs_path)


def clear_db_backup():
    db_path = os.getcwd() + '/backup/'
    clear_files(db_path)


def clear_files(paths):
    valid_days = 7
    c_t = time.gmtime()
    c_st = time.strftime('%Y-%m-%d', c_t)
    c_year, c_month, c_day = c_st.split('-')
    c_td = datetime.datetime(int(c_year), int(c_month), int(c_day))

    if not os.path.exists(paths):
        return

    file_list = os.listdir(paths)
    for f in file_list:
        t = time.gmtime(os.stat('{}/{}'.format(paths, f))[stat.ST_CTIME])   # file create time
        st = time.strftime('%Y-%m-%d', t)
        year, month, day = st.split('-')
        td = datetime.datetime(int(year), int(month), int(day))
        days = (c_td - td).days
        if days >= valid_days:
            f_path = '{}/{}'.format(paths, f)
            try:
                if f_path.strip() == '/':
                    continue
                os.remove(f_path)
            except Exception as e:
                func.log_error('[gate] clear_logs f_path: {}, failed: {}'.format(f_path, e.message))


def backup_db():
    today = datetime.date.today()
    backup_path = os.getcwd() + '/backup/'
    if not os.path.exists(backup_path):
        os.makedirs(backup_path)
    backup_file_name_tar = '{}{}_{}.tar.gz'.format(backup_path, constant.DB_NAME, today)
    if os.path.isfile(backup_file_name_tar):
        func.log_info('[gate] backup_db file: {} is exist'.format(backup_file_name_tar))
        return
    backup_file_name = '{}{}_{}.sql'.format(backup_path, constant.DB_NAME, today)
    try:
        cmd = 'mysqldump -h{} -u{} -p{} {} --default_character-set={} > {}'.format(
                constant.DB_HOST, constant.DB_USER, constant.DB_PASSWD, constant.DB_NAME, 'utf8', backup_file_name)
        os.system(cmd)
        # tar
        tar = tarfile.open(backup_file_name_tar, 'w:gz')
        for root, _, files in os.walk(backup_path):
            for f in files:
                if 'sql' not in f:
                    continue
                full_path = os.path.join(root, f)
                tar.add(full_path, arcname=f)
        tar.close()
    except Exception as e:
        func.log_error('[gate] backup_db failed: {}'.format(e.message))
    finally:
        os.system('rm -rf {}'.format(backup_file_name))

