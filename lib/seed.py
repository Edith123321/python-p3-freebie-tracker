#!/usr/bin/env python3

# Import the necessary modules and classes
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Company, Dev, Freebie

engine = create_engine('sqlite:///freebies.db')

# Bind the engine to the Base metadata
Base.metadata.bind = engine

# Create a session
Session = sessionmaker(bind=engine)
session = Session()


#  sample companies
company1 = Company(name="Moringa School", founding_year=2000)
company2 = Company(name="Anave beauty", founding_year=1995)

#  sample devs
dev1 = Dev(name="Edith")
dev2 = Dev(name="Bob")
dev3 = Dev(name = 'Lucy')

#  sample freebies
freebie1 = Freebie(item_name="Laptop", value=1000, dev=dev1, company=company1)
freebie2 = Freebie(item_name="Mouse", value=50, dev=dev2, company=company2)
freebie3 = Freebie(item_name = 'Water bottle', value = 250, dev= dev3, company = company1)

# Add data to the session
session.add_all([company1, company2, dev1, dev2,dev3,  freebie1, freebie2, freebie3])

# Commit the changes to the database
session.commit()


