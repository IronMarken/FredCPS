import DBcontroller
import APImanager
import supportFunctions


def init_db():
    DBcontroller.setup_db()


# retrieve categories in a tree structure
def get_category(category_id, update_tree, token):
    # if the category is in the DB also subtree is present
    if update_tree or not DBcontroller.category_exists(category_id):
        return supportFunctions.download_category(category_id, token)
    else:
        return DBcontroller.get_category(category_id)


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
    return category


# retrieve category series
def get_series(category_id, update, token):
    if update:
        return supportFunctions.download_series(category_id, token)
    else:
        return DBcontroller.get_series(category_id)


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
    if update:
        return supportFunctions.download_observations(series_id, token)
    else:
        return DBcontroller.get_observations(series_id)
