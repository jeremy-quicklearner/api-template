import sqlalchemy as sa
from sqlalchemy import orm as sa_orm
from sqlalchemy.inspection import inspect as sa_inspect

from . import types

db = sa.create_engine('sqlite:///runtime/db.sqlite3', echo=True)
types.declBase.metadata.create_all(db)

session = sa_orm.Session(db)

def finalize():
    session.close()
    db.dispose()

# Generic CRUD
def get(type, pkVal):
    return session.get(type, pkVal)

def createOrUpdate(record):
    merged = session.merge(record)
    session.commit()
    return merged.id

def delete(type, pkVal):
    record = get(type, pkVal)
    session.delete(record)
    session.commit()

# Type-specific
def findBooksByPersonName(name):
    query = sa.select(
        types.Person, types.PersonOwnsBook, types.Book,
    ).filter(
        types.Person.name == name,
    ).filter(
        types.Person.id == types.PersonOwnsBook.personId,
    ).filter(
        types.Book.id == types.PersonOwnsBook.bookId
    )
    results = session.execute(query)
    return [r[2] for r in results.all()]
