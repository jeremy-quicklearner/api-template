from . import types
from . import data

class Logic(object):
    # Logic layer
    def __init__(self):
        self.data = data.Data()

    def finalize(self):
        self.data.finalize()

    # Generic CRUD
    def get(self, type, pkVal):
        return self.data.get(type, pkVal)

    def createOrUpdate(self, record):
        return self.data.createOrUpdate(record)

    def delete(self, type, pkVal):
        return self.data.delete(type, pkVal)

    # Type-Specific
    def findBooksByPersonName(self, name):
        return self.data.findBooksByPersonName(name)
