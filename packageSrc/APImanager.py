from datetime import datetime
import math

import constUtil
import json
import requests
import time
from structUtils import *


def get_json_data(complete_url):
    connection = requests.get(complete_url)
    text = connection.text
    data = json.loads(text)

    # raise exception
    if "error_code" in data:
        # Token limit exceeded
        if data["error_code"] == 429:
            # 120 requests limit in a minute
            print("Request limit exceeded...retrying after sleep")
            time.sleep(60)
            print("Retrying...")
            return get_json_data(complete_url)
        else:
            raise RuntimeError(data["error_code"], data["error_message"])
    return data


def get_my_category(category_id, token):
    complete_url = constUtil.OWN_CATEGORY % (category_id, token)

    data = get_json_data(complete_url)

    cat_id = data["categories"][0]["id"]
    name = data["categories"][0]["name"]
    parent = data["categories"][0]["parent_id"]
    return Category(cat_id, name, parent)


def get_children_category(category_id, token):
    complete_url = constUtil.CHILDREN_CATEGORY % (category_id, token)
    data = get_json_data(complete_url)

    ret_list = []
    for category in data["categories"]:
        child_id = category["id"]
        child_name = category["name"]
        child = Category(child_id, child_name, category_id)
        ret_list.append(child)
    return ret_list


def get_single_series(series_id, category_id, token):
    complete_url = constUtil.SINGLE_SERIES % (series_id, token)
    data = get_json_data(complete_url)
    series = data["seriess"]
    series_title = series["title"]
    return Series(series_id, series_title, category_id)


def get_category_from_series(series_id, token):
    complete_url = constUtil.CATEGORY_FROM_SERIES % (series_id, token)
    data = get_json_data(complete_url)
    cat_list = []
    for category in data["categories"]:
        category_id = category["id"]
        category_name = category["name"]
        category_parent = category["parent_id"]
        category = Category(category_id, category_name, category_parent)
        cat_list.append(category)
    return cat_list


def get_category_series(category_id, token):
    total = math.inf
    count = 0
    total_series = []
    while count < total:
        complete_url = constUtil.CATEGORY_SERIES % (category_id, token, count)
        data = get_json_data(complete_url)

        count += data["limit"]
        total = data["count"]

        for series in data["seriess"]:
            series_id = series["id"]
            series_title = series["title"]
            new_series = Series(series_id, series_title, category_id)
            total_series.append(new_series)
    return total_series


def get_series_observation(series_id, token):
    total = math.inf
    count = 0
    total_observations = []
    while count < total:
        complete_url = constUtil.SERIES_OBSERVATION % (series_id, token, count)
        data = get_json_data(complete_url)

        count += data["limit"]
        total = data["count"]

        for observation in data["observations"]:
            observation_date_str = observation["date"]
            observation_value_str = observation["value"]
            # NaN values
            if observation_value_str == ".":
                observation_value = math.nan
            else:
                observation_value = float(observation_value_str)
            observation_date = datetime.strptime(observation_date_str, '%y-%m-%d')
            new_observation = Observation(observation_date, observation_value, series_id)
            total_observations.append(new_observation)
    return total_observations
