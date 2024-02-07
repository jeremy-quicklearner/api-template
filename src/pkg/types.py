import sqlalchemy as sa
from sqlalchemy.ext import declarative as sa_decl

declBase = sa_decl.declarative_base()

class User(declBase):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String)

