from sqlalchemy import Column, String, Integer, Float, ForeignKey, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(tablename)s%(column_0name)s%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)
Base = declarative_base(metadata=metadata)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    username = Column(String())
    password = Column(String())
    income = Column(Float())
    #expense_id = Column(Integer(), ForeignKey("expenses.id")) ##PROBLEM LINE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    def __repr__(self):
        return f"Username: {self.username}, ID: {self.id}, Income: ${self.income}"
    

class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    amount = Column(Float())

    users = relationship("User", backref=backref("expense"))
    category = relationship('Category', backref=backref('expense'))

    def __repr__(self):
        return f"Name: {self.name}, ${self.amount}"

class Category(Base):
    __tablename__ = 'categories'
    id = Column('id', Integer, primary_key = True) 
    name = Column('name', String)
    expense = relationship('Expense', backref=backref('category'))
    
    def __repr__(self):
        return f"Name: {self.name}, ID: {self.id}"