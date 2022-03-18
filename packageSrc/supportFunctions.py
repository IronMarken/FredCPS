import numpy
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


def linear_interpolation(vector, j):
    if numpy.isnan(vector[0]) or numpy.isnan(vector[len(vector)-1]):
        print("First and/or last value is nan...not possible to apply linear interpolation")
        return vector

    # search left and right outliers
    i = 0
    while i < len(vector)-1:
        if numpy.isnan(vector[i+1]):
            t = position = i+1
            left_outlier_index = i
            left_outlier = vector[left_outlier_index]
            # search right outlier
            while t < len(vector):
                if not numpy.isnan(vector[t+1]):
                    right_outlier_index = t+1
                    right_outlier = vector[right_outlier_index]
                    print("left_outlier %s left index %d right_outlier %s right index %d\n" % (left_outlier, left_outlier_index, right_outlier, right_outlier_index))
                    vector = vector[:position]+[float(left_outlier + (right_outlier-left_outlier)/(right_outlier_index-left_outlier_index)*j)]+vector[position+1:]
                    break
                t += 1
        i += 1
    return vector
