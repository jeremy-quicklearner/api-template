from . import types
from . import data

def finalize():
    data.finalize()

# Generic CRUD
def get(type, pkVal):
    return data.get(type, pkVal)

def createOrUpdate(record):
    return data.createOrUpdate(record)

def delete(type, pkVal):
    return data.delete(type, pkVal)

# Type-Specific
def findBooksByPersonName(name):
    return data.findBooksByPersonName(name)
