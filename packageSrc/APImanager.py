import math

import constUtil
import json
import requests
from structUtils import *


def get_json_data(complete_url):
    connection = requests.get(complete_url)
    text = connection.text
    data = json.loads(text)

    # raise exception
    if "error_code" in data:
        raise RuntimeError(data["error_code"], data["error_message"])

    return data


def get_my_category(category_id, token):
    complete_url = constUtil.OWN_CATEGORY % (category_id, token)

    data = get_json_data(complete_url)

    cat_id = data["categories"][0]["id"]
    name = data["categories"][0]["name"]
    if category_id == 0:
        parent = None
    else:
        parent = data["categories"][0]["parent_id"]
    return Category(cat_id, name, parent)


# TODO add returned children to category struct and continue to the leafs
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
            observation_date = observation["date"]
            observation_value = observation["value"]
            # NaN values
            if observation_value == ".":
                observation_value = str(math.nan)
            new_observation = Observation(observation_date, observation_value, series_id)
            total_observations.append(new_observation)
    return total_observations