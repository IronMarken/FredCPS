import math
from datetime import datetime
import sqlite3
import os

import constUtil
from structUtils import *


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
    args = [cat_id, name, parent_id]
    execute_query(query, args)


def insert_series(ser_id, title, cat_ids):
    query = constUtil.INSERT_SERIES
    args = [ser_id, title]
    execute_query(query, args)
    query = constUtil.INSERT_CATEGORY_SERIES
    for cat_id in cat_ids:
        args = [cat_id, ser_id]
        execute_query(query, args)


def insert_observations(obs_date, value, series_id):
    query = constUtil.INSERT_OBSERVATION
    args = [obs_date, value, series_id]
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


def get_category(category_id):
    query = constUtil.GET_CATEGORY
    rows = execute_query(query, [category_id])
    return Category(category_id, rows[0][0], rows[0][1])


def get_series(category_id):
    query = constUtil.GET_SERIES
    rows = execute_query(query, [category_id])
    series_list = []
    for row in rows:
        series_id = row[0]
        series_name = row[1]
        new_series = Series(series_id, series_name, category_id)
        series_list.append(new_series)
    return series_list


def get_observations(series_id):
    query = constUtil.GET_OBSERVATIONS
    rows = execute_query(query, [series_id])
    observations_list = []
    for obs in rows:
        observation_date_str = obs[0]
        observation_value_str = obs[1]
        observation_date = datetime.strptime(observation_date_str, '%y-%m-%d')
        if observation_value_str == 'nan':
            observation_value = math.nan
        else:
            observation_value = float(observation_value_str)
        new_observation = Observation(observation_date, observation_value, series_id)
        observations_list.append(new_observation)
    return observations_list
