import DBcontroller
import APImanager


# update or download all the subtree
def recursive_leaf_category(children_list, token):
    for child in children_list:
        DBcontroller.insert_category(child.id, child.name, child.parent_id)
        # all from API because on DB I can have only partial children
        children = APImanager.get_children_category(child.id, token)
        recursive_leaf_category(children, token)
    return


def download_category(category_id, token):
    my_category = APImanager.get_my_category(category_id, token)
    DBcontroller.insert_category(my_category.id, my_category.name, my_category.parent_id)
    children = APImanager.get_children_category(category_id, token)
    recursive_leaf_category(children, token)
    return my_category


def download_series(category_id, token):
    series = APImanager.get_category_series(category_id, token)
    for ser in series:
        DBcontroller.insert_series(ser.id, ser.title, [ser.category_id])
    return series


def download_observations(series_id, token):
    observations = APImanager.get_series_observation(series_id, token)
    for obs in observations:
        DBcontroller.insert_observations(str(obs.date), str(obs.value), series_id)
    return observations
