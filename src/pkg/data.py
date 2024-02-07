import sqlalchemy as sa
from sqlalchemy import orm as sa_orm
from sqlalchemy.inspection import inspect as sa_inspect

from . import types

class Data(object):

    # Data layer
    def __init__(self):
        self.db = sa.create_engine('sqlite:///runtime/db.sqlite3', echo=True)
        types.declBase.metadata.create_all(self.db)

        self.session = sa_orm.Session(self.db)

    def finalize(self):
        self.session.close()
        self.db.dispose()

    # Generic CRUD
    def get(self, type, pkVal):
        return self.session.get(type, pkVal)

    def createOrUpdate(self, record):
        self.session.merge(record)
        self.session.commit()

    def delete(self, type, pkVal):
        record = self.get(type, pkVal)
        self.session.delete(record)
        self.session.commit()

    # Type-specific
    def findUsersByName(self, name):
        query = sa.select(types.User).filter(types.User.name == name)
        results = self.session.execute(query)
        return [r[0] for r in results.all()]
