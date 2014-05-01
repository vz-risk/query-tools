class SQLMaterializer(object):

    def __init__(self):
        pass

    def make_session(self):
        return SQLMaterializerSession()

    def setup(self):
        pass

class SQLMaterializerSession(object):

    def __init__(self):
        pass

    def add_all(self, domain_objects):
        pass

    def query(self, criteria):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass
