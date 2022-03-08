import DBcontroller
import APImanager
import time


def init_db():
    DBcontroller.setup_db()


def recursive_leaf(children_list, token, update):
    for child in children_list:
        if update or not DBcontroller.category_exists(child.id):
            DBcontroller.insert_category(child.id, child.name, child.parent_id)
            # all from API because on DB I can have only partial children
            try:
                children = APImanager.get_children_category(child.id, token)
                recursive_leaf(children, token, update)
            except RuntimeError as error:
                # Requests limit exceed
                if error.args[0] == 429:
                    # 120 requests limit in a minute
                    print("Request limit exceeded...retrying after sleep")
                    time.sleep(60)
                    print("Retrying...")
                    children = APImanager.get_children_category(child.id, token)
                    recursive_leaf(children, token, update)
                else:
                    raise error
    return


# retrieve categories in a tree structure
def get_category(category_id, update, token):
    # if the category is in the DB also subtree is present
    if update or not DBcontroller.category_exists(category_id):
        my_category = APImanager.get_my_category(category_id, token)
        DBcontroller.insert_category(my_category.id, my_category.name, my_category.parent_id)
        children = APImanager.get_children_category(category_id, token)
        recursive_leaf(children, token, update)
