# coding:utf8
from numbers import Number
from firefly.dbentrust.dbutils import safestr
from app.util.driver import dbpool
from app.util.common import func


db_pool = dbpool.DBPool()


def insert_update_record(**kwargs):
    """
    插入语句, 如果已经存在,则更新
    :param kwargs:
            {
                'table': table_name
                'data': {field_name: field_value, ...}
            }
    :return:
    """
    field_list, value_list = _format_insert_sql(kwargs.get('data'))
    sql = "insert into {table_name} ({fields}) values ({values}) on duplicate key update {pre} ".format(
            table_name=kwargs.get('table'), fields=field_list, values=value_list,
            pre=_format_update_sql(kwargs.get("data"))
    )
    return execute(sql)


def insert_record(**kwargs):
    """
    插入语句, 如果已存在,则失败
    :param kwargs:
            {
                'table': table_name
                'data': {field_name: field_value, ...}
            }
    :return:
    """
    field_list, value_list = _format_insert_sql(kwargs.get('data'))
    sql = "insert into {} ({}) VALUES ({})".format(
            safestr(kwargs.get('table')), safestr(field_list), safestr(value_list))
    return execute(sql)


def insert_auto_increment_record(**kwargs):
    """
    插入语句, 并返回自增长ID
    :param kwargs:
            {
                'table': table_name
                'data': {field_name: field_value, ...}
            }
    :return:
    """
    field_list, value_list = _format_insert_sql(kwargs.get('data'))
    sql = "insert into {} ({}) VALUES ({})".format(
            safestr(kwargs.get('table')), safestr(field_list), safestr(value_list))
    return execute_auto_increment(sql)


def update_record(**kwargs):
    """
    更新, 如果不存在, 则失败
    :param kwargs:
            {
                'table': table_name
                'where': {field_name: field_value}
                'data': {field_name: field_value, ...}
            }
    :return:
    """
    where = _format_condition(kwargs.get('where'))
    update = _format_update_sql(kwargs.get('data'))
    sql = "update {} set {} {}".format(safestr(kwargs.get('table')), safestr(update), safestr(where))
    return execute(sql)


def execute(sql):
    if not isinstance(sql, list):
        flag = db_pool.execute_sql(sql)
    else:
        flag = db_pool.execute_multi_sql(sql)
    return flag


def execute_auto_increment(sql):
    return db_pool.execute_auto_increment(sql)


def query_one(sql):
    return db_pool.query_one(sql, True)


def query_all(sql):
    return db_pool.query_all(sql, True)


def _for_each_field_props(props):
    """
    遍历字段列表生成sql语句
    :param props:
    :return:
    """
    sql = ''
    if props == '*':
        return '*'
    elif isinstance(props, list):
        for prop in props:
            sql = sql + prop + ','
        sql = sql[:-1]
        return sql
    else:
        func.log_error('[each_query_props] props {} must be list'.format(props))
        return sql


def _for_each_update_props(sql, props):
    """
    遍历所要修改的属性，以生成sql语句
    :param sql: "update `table_name` set"
    :param props: {field_name: field_value, ...}
    :return:
    """
    if isinstance(props, dict):
        i = 0
        for columnName, columnValue in props.items():
            if isinstance(columnValue, basestring):
                if i == 0:
                    sql += " %s=\"%s\"" % (columnName, columnValue)
                else:
                    sql += ", %s=\"%s\"" % (columnName, columnValue)
            else:
                if i == 0:
                    sql += " %s=%s" % (columnName, columnValue)
                else:
                    sql += ", %s=%s" % (columnName, columnValue)
            i += 1
    return sql


def _convert_str(s):
    return safestr(s).replace("'", "\\'")


def _format_insert_sql(props):
    """
    生成插入语句
    :param props:
    :return:
    """
    field_list = []
    value_list = []
    for field, value in props.items():
        field_list.append("`%s`" % field)
        if isinstance(value, Number):
            value_list.append("%s" % value)
        else:
            value_list.append("'%s'" % _convert_str(value))
    return ",".join(field_list), ",".join(value_list)


def _format_update_sql(props):
    """
    生成更新语句
    :param props:
    :return:
    """
    l = []
    for field, value in props.items():
        if isinstance(value, Number):
            sql = "`{}`={}".format(field, value)
        else:
            sql = "`{}`='{}'".format(field, _convert_str(value))
        l.append(sql)
    return ','.join(l)


def _format_condition(props):
    """
    生成查询条件字符串
    :param props:
    :return:
    """
    if not props:
        return ""
    if isinstance(props, dict):
        props_list = []
        for _item in props.items():
            if isinstance(_item[1], Number):
                sql = "`%s`=%s" % _item
            elif isinstance(_item[1], list):
                symbol = str(_item[1][0]).lower()
                val = _item[1][1]
                if symbol == "in" or symbol == "not in":
                    if isinstance(val, list) or isinstance(val, tuple):
                        sql = "`%s` %s ('%s')" % (_item[0], symbol, "','".join(map(str, val)))
                    else:
                        sql = "`%s` %s (%s)" % (_item[0], symbol, _convert_str(val))
                else:
                    if isinstance(val, Number):
                        sql = "`%s` %s %s" % (_item[0], symbol, val)
                    else:
                        sql = "`%s` %s '%s'" % (_item[0], symbol, _convert_str(val))
            else:
                sql = "`%s`='%s'" % (_item[0], _convert_str(_item[1]))
            props_list.append(sql)
        where = ' AND '.join(props_list)
    else:
        where = safestr(props)
    return " WHERE %s" % where


if __name__ == '__main__':
    # execute
    data = {
        "uuid": "123456",
        "cid": 0,
        "user_name": "Stu",
        "password": "1",
        "token_key": "098765"
    }
    account_id = insert_auto_increment_record(**{
        'table': 'account',
        'data': data
    })

