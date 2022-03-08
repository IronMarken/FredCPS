import sqlite3

import constUtil
import os


def setup_db():
    # check if dir exists
    if not os.path.isdir(constUtil.DB_PATH):
        os.mkdir(constUtil.DB_PATH)

    # check if db file exists
    if not os.path.exists(constUtil.FULL_PATH):
        open(constUtil.FULL_PATH, 'w')
        generate_tables()


def get_connection():
    conn = None
    try:
        conn = sqlite3.connect(constUtil.FULL_PATH)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn


def generate_tables():
    conn = get_connection()
    if conn is not None:
        try:
            c = conn.cursor()
            for table in constUtil.TABLES_LIST:
                c.execute(table)
        except sqlite3.Error as e:
            print(e)
        conn.close()


def execute_query(query, args):
    conn = get_connection()
    data = None
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute(query, args)
            data = c.fetchall()
        except sqlite3.Error as e:
            print(e)
        conn.commit()
        conn.close()
        return data


def insert_category(cat_id, name, parent_id):
    query = constUtil.INSERT_CATEGORY
    args = [cat_id, name]
    execute_query(query, args)
    args = [cat_id, parent_id]
    query = constUtil.INSERT_PARENT
    execute_query(query, args)


def insert_series(ser_id, title, cat_id):
    query = constUtil.INSERT_SERIES
    args = [ser_id, title, cat_id]
    execute_query(query, args)


def insert_observations(date, value, series_id):
    query = constUtil.INSERT_OBSERVATION
    args = [date, value, series_id]
    execute_query(query, args)


def truncate_table(table_name):
    query = constUtil.TRUNCATE
    execute_query(query, [table_name])


def category_exists(category_id):
    query = constUtil.CATEGORY_EXISTS
    rows = execute_query(query, [category_id])
    if not rows:
        return False
    else:
        return True


def series_exists(series_id):
    query = constUtil.SERIES_EXISTS
    rows = execute_query(query, [series_id])
    if not rows:
        return False
    else:
        return True


def observation_exists(observation_date):
    query = constUtil.OBSERVATION_EXISTS
    rows = execute_query(query, [observation_date])
    if not rows:
        return False
    else:
        return True
