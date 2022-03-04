import DBcontroller
import APImanager

def init_db():
    DBcontroller.setup_db()

# retrieve categories from another one
def get_category(category_id, update):
    # download from API only new
    if not update:

