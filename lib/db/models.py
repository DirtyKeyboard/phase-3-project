from sqlalchemy import Column, String, Integer, Float, ForeignKey, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

engine = create_engine("sqlite:///database.db")
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    username = Column(String())
    password = Column(String())
    income = Column(Float())
    expenses = relationship('Expense', back_populates='user')
    categories = association_proxy('expenses', 'category',
        creator=lambda c: Expense(category=c))

    def __repr__(self):
        return f"Username: {self.username}, ID: {self.id}, Income: ${self.income}"
    

class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    amount = Column(Float())
    user_id = Column(Integer(), ForeignKey("users.id"))
    category_id = Column(Integer(), ForeignKey("categories.id"))

    user = relationship('User', back_populates='expenses')
    category = relationship('Category', back_populates='expenses')

    def __repr__(self):
        return f"Name: {self.name}, ${self.amount}"

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer(), primary_key = True) 
    name = Column(String())
    expenses = relationship('Expense', back_populates='category')

    users = association_proxy('expenses', 'user',
        creator=lambda u: Expense(user=u))
    
    def __repr__(self):
        return f"Name: {self.name}, ID: {self.id}"