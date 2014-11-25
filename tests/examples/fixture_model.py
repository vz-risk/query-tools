class Penguin(object):
    
    def __init__(self, name, mood, id=None):
        self.name = name
        self.mood = mood
        self.id = id

    def __repr__(self):
        return '< %s the %s penguin >' % (self.name, self.mood)

class Goose(object):

    def __init__(self, name, favorite_penguin, id=None):
        self.name = name
        self.favorite_penguin = favorite_penguin
        self.id = id

    def __repr__(self):
        template = '< %s, the goose that likes %s >'
        return template % (self.name, repr(self.favorite_penguin))

