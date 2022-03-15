import DBcontroller
import APImanager
import supportFunctions


def init_db():
    DBcontroller.setup_db()


# retrieve categories in a tree structure
def get_category(category_id, update_tree, token):
    # if the category is in the DB also subtree is present
    if update_tree or not DBcontroller.category_exists(category_id):
        my_category = APImanager.get_my_category(category_id, token)
        DBcontroller.insert_category(my_category.id, my_category.name, my_category.parent_id)
        children = APImanager.get_children_category(category_id, token)
        supportFunctions.recursive_leaf_category(children, token, update_tree)


# update single category
def update_category(category_id, token):
    # update category data
    category = APImanager.get_my_category(category_id, token)
    DBcontroller.insert_category(category.id, category.name, category.parent_id)

    # update category series
    series = get_series(category_id, True, token)

    # update observations
    for ser in series:
        get_observations(ser.id, True, token)


# retrieve category series
def get_series(category_id, update, token):
    series = APImanager.get_category_series(category_id, token)
    for ser in series:
        if update or not DBcontroller.series_exists(ser.id):
            DBcontroller.insert_series(ser.id, ser.title, [ser.category_id])
    return series


# update series
def update_series(series_id, token):
    # retrieve series categories and insert series updated
    categories = APImanager.get_category_from_series(series_id, token)
    for category in categories:
        DBcontroller.insert_category(category.id, category.name, category.parent_id)
        series = APImanager.get_single_series(series_id, category.id, token)
        DBcontroller.insert_series(series.id, series.title, series.category_id)

    # update series observations
    get_observations(series_id, True, token)


# retrieve observations from a series
def get_observations(series_id, update, token):
    observations = APImanager.get_series_observation(series_id, token)
    for obs in observations:
        if update or not DBcontroller.observation_exists(obs.date):
            DBcontroller.insert_observations(obs.date, obs.value, series_id)
