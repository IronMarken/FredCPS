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


def execute_query(query):
    conn = get_connection()
    data = None
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute(query)
            data = c.fetchall()
        except sqlite3.Error as e:
            print(e)
        conn.commit()
        conn.close()
        return data


def insert_category(cat_id, name, parent_id=None):
    query = constUtil.INSERT_CATEGORY % (cat_id, name)
    execute_query(query)
    if parent_id is not None:
        query = constUtil.INSERT_PARENT % (cat_id, parent_id)
        execute_query(query)


def insert_series(ser_id, title, cat_id):
    query = constUtil.INSERT_SERIES % (ser_id, title, cat_id)
    execute_query(query)


def insert_observations(date, value, series_id):
    query = constUtil.INSERT_OBSERVATION % (date, value, series_id)
    execute_query(query)


def truncate_table(table_name):
    query = constUtil.TRUNCATE % table_name
    execute_query(query)


def category_exists(category_id):
    query = constUtil.CATEGORY_EXISTS % category_id
    rows = execute_query(query)
    if not rows:
        return False
    else:
        return True


def series_exists(series_id):
    query = constUtil.SERIES_EXISTS % series_id
    rows = execute_query(query)
    if not rows:
        return False
    else:
        return True


def observation_exists(observation_date):
    query = constUtil.OBSERVATION_EXISTS % observation_date
    rows = execute_query(query)
    if not rows:
        return False
    else:
        return True
