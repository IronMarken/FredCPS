import os

# DB constants
DB_PATH = os.path.dirname(os.path.abspath(__file__))+"/../db"
DB_NAME = "FredData.db"
FULL_PATH = DB_PATH + "/" + DB_NAME

# DB tables
CATEGORY_TABLE = """ CREATE TABLE IF NOT EXISTS category(
                                        id INTEGER PRIMARY KEY,
                                        name TEXT,
                                        parent_id INTEGER);"""

CATEGORY_SERIES_TABLE = """ CREATE TABLE IF NOT EXISTS category_series(
                                        category_id INTEGER,
                                        series_id INTEGER,
                                        PRIMARY KEY (category_id, series_id),
                                        FOREIGN KEY (category_id) REFERENCES category(id)
                                        ON DELETE CASCADE ON UPDATE CASCADE,
                                        FOREIGN KEY (series_id) REFERENCES series(id)
                                        ON DELETE CASCADE ON UPDATE CASCADE );"""

SERIES_TABLE = """ CREATE TABLE IF NOT EXISTS series(
                                        id TEXT PRIMARY KEY,
                                        title TEXT);"""


OBSERVATIONS_TABLE = """ CREATE TABLE IF NOT EXISTS observations(
                                        observationDate DATE PRIMARY KEY,
                                        value TEXT,
                                        series_id TEXT,
                                        FOREIGN KEY (series_id) REFERENCES series (id) 
                                        ON DELETE CASCADE ON UPDATE CASCADE );"""

TABLES_LIST = [CATEGORY_TABLE, SERIES_TABLE, OBSERVATIONS_TABLE, CATEGORY_SERIES_TABLE]
TABLE_NAMES = ["category", "category_series", "series", "observations"]

INSERT_CATEGORY = """ insert or replace into category(id, name, parent_id) values(?, ?, ?)"""
INSERT_CATEGORY_SERIES = """insert or replace into category_series(category_id, series_id) values(?, ?)"""
INSERT_SERIES = """ insert or replace into series(id, title) values(?, ?)"""
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

# add series_id and token_api
SINGLE_SERIES = "https://api.stlouisfed.org/fred/series?series_id=%s&api_key=%s&file_type=json"

# add series_id and token_api
CATEGORY_FROM_SERIES = "https://api.stlouisfed.org/fred/series/categories?series_id=%s&api_key=%s&file_type=json"

# add series_id, offset and token_api
SERIES_OBSERVATION = "https://api.stlouisfed.org/fred/series/observations?series_id=%s&api_key=%s&offset=%d&file_type" \
                     "=json"
