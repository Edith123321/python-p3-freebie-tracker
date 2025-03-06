from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    def __repr__(self):
        return f'<Company {self.name}>'

    # One company has many freebies
    freebies = relationship('Freebie', back_populates='company')

    # Class method to find the oldest company
    @classmethod
    def oldest_company(cls):
        return cls.query.order_by(cls.founding_year).first()

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name = Column(String())

    def __repr__(self):
        return f'<Dev {self.name}>'

    # One dev can have many freebies
    freebies = relationship('Freebie', back_populates='dev')  # Corrected to 'dev'

    # Function to check if a dev received a specific freebie
    def received_one(self, item_name):
        return any(freebie.item_name == item_name for freebie in self.freebies)

    # Function to give away a freebie
    def give_away(self, dev, freebie):
        if freebie in self.freebies:
            freebie.dev = dev

class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer, primary_key=True)
    item_name = Column(String)
    value = Column(Integer)

    # Foreign keys to link to devs and companies
    dev_id = Column(Integer, ForeignKey('devs.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))

    def __repr__(self):
        return f"<Freebie: {self.item_name}>"

    # Many freebies can belong to one company
    company = relationship('Company', back_populates='freebies')

    # A single freebie belongs to one dev
    dev = relationship('Dev', back_populates='freebies') 

     #function to print the details
    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"
    
# print(Freebie.print_details())

oldest = Company.oldest_company()
print(f"The oldest company is {oldest.name}, founded in {oldest.founding_year}.")
