# root (0) has empty parent_id
class Category:
    def __init__(self, category_id, category_name, parent_id):
        self.id = category_id
        self.name = category_name
        self.parent_id = parent_id

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'parent': self.parent_id
        }


# series struct
class Series:
    def __init__(self, series_id, series_title, category_id):
        self.id = series_id
        self.title = series_title
        self.category_id = category_id

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category_id
        }


# observation struct
class Observation:
    def __init__(self, observation_date, observation_value, series_id):
        self.date = observation_date
        self.value = observation_value
        self.series_id = series_id

    def to_dict(self):
        return {
            'date': self.date,
            'value': self.value,
            'series': self.series_id
        }
