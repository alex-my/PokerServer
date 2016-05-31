# coding:utf8
import MySQLdb
import Queue
from app.util.common import func


class DBPoolException(Exception):
    pass


class DBCursor(object):

    def __init__(self, conn, cursor_class):
        self._conn = conn
        if cursor_class:
            self._cursor = conn.cursor(cursorclass=cursor_class)
        else:
            self._cursor = conn.cursor()

    def execute(self, sql):
        return self._cursor.execute(sql)

    def fetch_all(self):
        return self._cursor.fetchall()

    def fetch_one(self):
        return self._cursor.fetchone()

    def close(self):
        self._cursor.close()
        self._conn.close()
        self._cursor = None
        self._conn = None


class DBPool(object):

    def __init__(self):
        self._free_connections = None
        self._max_wait = None
        self._db_type = None
        self._config = None
        self._cur_conn = None

    def init_db_pool(self, max_active=5, max_wait=5, init_size=1, db_type='mysql', **config):
        func.log_info('[DBPool] init_db_pool {}'.format(config))
        self._free_connections = Queue.Queue(max_active)
        self._max_wait = max_wait
        self._db_type = db_type
        self._config = config
        for _ in xrange(init_size):
            self.free_conn(self.create_conn())
        self._cur_conn = None

    def __del__(self):
        func.log_info('[DBPool] del')
        self.release_all_conns()

    def release_all_conns(self):
        pass

    def free_conn(self, conn):
        conn.pool = None
        if self._free_connections.full():
            conn.release()
        else:
            self._free_connections.put_nowait(conn)

    def get_conn(self, timeout=None):
        if timeout is None:
            timeout = self._max_wait
        if self._free_connections.empty():
            conn = self.create_conn()
        else:
            conn = self._free_connections.get(timeout=timeout)
            conn.pool = self
        return conn

    def create_conn(self):
        return MySQLdb.connect(**self._config)

    def cursor(self, cursor_class=None):
        conn = self.get_conn()
        self._cur_conn = conn
        return DBCursor(conn, cursor_class)

    def commit(self):
        try:
            self._cur_conn.commit()
        except Exception as e:
            func.log_exception('[DBPool] commit exception: {}'.format(e.message))

    def rollback(self):
        try:
            self._cur_conn.rollback()
        except Exception as e:
            func.log_exception('[DBPool] rollback exception: {}'.format(e.message))

    def execute_sql(self, sql):
        conn = self.get_conn(5)
        cursor = conn.cursor()
        try:
            count = cursor.execute(sql)
            conn.commit()
            cursor.close()
            conn.close()
            return count
        except Exception as e:
            cursor.close()
            conn.close()
            func.log_exception('[DBPool] execute_sql exception: {}, sql: {}'.format(e.message, sql))
            return None

    def execute_auto_increment(self, sql):
        conn = self.get_conn(5)
        cursor = conn.cursor()
        try:
            count = cursor.execute(sql)
            conn.commit()
            if count > 0:
                increment_id = cursor.lastrowid
            else:
                increment_id = 0
            cursor.close()
            conn.close()
            return increment_id
        except Exception as e:
            cursor.close()
            conn.close()
            func.log_exception('[DBPool] execute_auto_increment exception: {}, sql: {}'.format(e.message, sql))
            return None

    def execute_multi_sql(self, sql_list):
        conn = self.get_conn(5)
        cursor = conn.cursor()
        try:
            conn.autocommit(False)
            for sql in sql_list:
                count = cursor.execute(sql)
                if count < 0:
                    raise
            else:
                conn.commit()
                conn.autocommit(True)
                cursor.close()
                conn.close()
                return True
        except Exception as e:
            conn.rollback()
            conn.autocommit(True)
            cursor.close()
            conn.close()
            func.log_exception('[DBPool] execute_sql exception: {}, sql_list: {}'.format(e.message, sql_list))
            return False

    def query_all(self, sql, dict_cursor=False):
        conn = self.get_conn(0)
        if dict_cursor:
            cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        else:
            cursor = conn.cursor()
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return results
        except Exception as e:
            cursor.close()
            conn.cursor()
            func.log_exception('[DBPool] query_all exception: {}, sql: {}'.format(e.message, sql))
            return None

    def query_one(self, sql, dict_cursor=False):
        conn = self.get_conn(0)
        if dict_cursor:
            cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        else:
            cursor = conn.cursor()
        try:
            cursor.execute(sql)
            results = cursor.fetchone()
            cursor.close()
            conn.close()
            return results
        except Exception as e:
            cursor.close()
            conn.cursor()
            func.log_exception('[DBPool] query_one exception: {}, sql: {}'.format(e.message, sql))
            return None
