#!/usr/bin/env python3
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker



from db.models import User, Expense, Category, Base



if __name__ == '__main__':

    engine = create_engine('sqlite:///database.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    

    import ipdb; ipdb.set_trace()