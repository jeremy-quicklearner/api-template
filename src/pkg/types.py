import sqlalchemy as sa
from sqlalchemy.ext import declarative as sa_decl

declBase = sa_decl.declarative_base()
def structify(record):
    return {c.name:getattr(record, c.name) for c in record.__table__.columns}

class Person(declBase):
    __tablename__ = 'person'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String)

class Book(declBase):
    __tablename__ = 'book'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String)
    publisher = sa.Column(sa.String)

class PersonOwnsBook(declBase):
    __tablename__ = 'person_owns_book'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    personId = sa.Column(sa.Integer, sa.ForeignKey('person.id'))
    bookId = sa.Column(sa.Integer, sa.ForeignKey('book.id'))
