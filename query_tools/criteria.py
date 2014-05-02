class Criteria(object):

    def __init__(self, path, value, operator='in'):
        self.path = path
        self.value = value
        self.operator = operator

class Conjuction(object):

    def __init__(self, conjuction, criteria):
        self.conjuction = conjunction
        self.criteria = criteria

    def __iter__(self):
        return iter(self.critera)
