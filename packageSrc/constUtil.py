import os

# DB constants
DB_PATH = os.path.dirname(os.path.abspath(__file__))+"/../db"
DB_NAME = "FredData.db"
FULL_PATH = DB_PATH + "/" + DB_NAME

# DB tables
CATEGORY_TABLE = """ CREATE TABLE IF NOT EXISTS category(
                                        id INTEGER PRIMARY KEY,
                                        name TEXT);"""

PARENT_TABLE = """ CREATE TABLE IF NOT EXISTS parents(
                                        child_id INTEGER PRIMARY KEY,
                                        parent_id INTEGER,
                                        FOREIGN KEY (parent_id) REFERENCES category(id)
                                        ON DELETE CASCADE ON UPDATE CASCADE,
                                        FOREIGN KEY (child_id) REFERENCES category(id)
                                        ON DELETE CASCADE ON UPDATE CASCADE );"""

SERIES_TABLE = """ CREATE TABLE IF NOT EXISTS series(
                                        id TEXT PRIMARY KEY,
                                        title TEXT,
                                        category_id INTEGER,
                                        FOREIGN KEY (category_id) REFERENCES category (id) 
                                        ON DELETE CASCADE ON UPDATE CASCADE );"""


OBSERVATIONS_TABLE = """ CREATE TABLE IF NOT EXISTS observations(
                                        observationDate DATE PRIMARY KEY,
                                        value TEXT,
                                        series_id TEXT,
                                        FOREIGN KEY (series_id) REFERENCES series (id) 
                                        ON DELETE CASCADE ON UPDATE CASCADE );"""

TABLES_LIST = [CATEGORY_TABLE, SERIES_TABLE, OBSERVATIONS_TABLE, PARENT_TABLE]
TABLE_NAMES = ["category", "parents", "series", "observations"]

INSERT_CATEGORY = """ insert or replace into category(id, name) values(?, ?)"""
INSERT_PARENT = """insert or replace into parents(child_id, parent_id) values(?, ?)"""
INSERT_SERIES = """ insert or replace into series(id, title, category_id) values(?, ?, ?)"""
INSERT_OBSERVATION = """insert or replace into observations(observationDate, value, series_id) values(?, ?, ?)"""

# add table name
TRUNCATE = """delete from ?;"""

CATEGORY_EXISTS = """select distinct id from category where id=?"""
SERIES_EXISTS = """select distinct id from series where id=?"""
OBSERVATION_EXISTS = """select distinct observationDate from observations where observationDate=?"""


# add category_id, offset and token_api
OWN_CATEGORY = "https://api.stlouisfed.org/fred/category?category_id=%d&api_key=%s&file_type=json"
CHILDREN_CATEGORY = "https://api.stlouisfed.org/fred/category/children?category_id=%d&api_key=%s&file_type=json"
CATEGORY_SERIES = "https://api.stlouisfed.org/fred/category/series?category_id=%d&api_key=%s&offset=%d&file_type=json"

# add series_id, offset and token_api
SERIES_OBSERVATION = "https://api.stlouisfed.org/fred/series/observations?series_id=%s&api_key=%s&offset=%d&file_type" \
                     "=json"
