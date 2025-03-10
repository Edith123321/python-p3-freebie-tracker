from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref, session
from sqlalchemy.ext.declarative import declarative_base

# Define naming conventions for foreign keys
convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

# Create the base class
Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    # One company has many freebies
    freebies = relationship('Freebie', back_populates='company')

    # One company can give many freebies

    devs = relationship('Dev', secondary='freebies', back_populates='companies')

    def __repr__(self):
        return f'<Company {self.name}>'

    # Class method to find the oldest company
    @classmethod
    def oldest_company(cls):
        return session.query(cls).order_by(cls.founding_year).first()

    # Method to give a freebie to a dev
    def give_freebie(self, dev, item_name, value):
        freebie = Freebie(item_name=item_name, value=value, dev=dev, company=self)
        session.add(freebie)
        session.commit()
        return freebie

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name = Column(String())

    # One dev has many freebies
    freebies = relationship('Freebie', back_populates='dev')

    # One dev has many companies through freebies
    companies = relationship('Company', secondary='freebies', back_populates='devs')

    def __repr__(self):
        return f'<Dev {self.name}>'

    # Method to check if a dev received a specific freebie
    def received_one(self, item_name):
        return any(freebie.item_name == item_name for freebie in self.freebies)

    # Method to give away a freebie to another dev
    def give_away(self, dev, freebie):
        if freebie in self.freebies:
            freebie.dev = dev
            session.commit()

class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer, primary_key=True)
    item_name = Column(String)
    value = Column(Integer)

    # Foreign keys to link to devs and companies
    dev_id = Column(Integer, ForeignKey('devs.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))

    # Relationships
    dev = relationship('Dev', back_populates='freebies')
    company = relationship('Company', back_populates='freebies')

    def __repr__(self):
        return f"<Freebie: {self.item_name}>"

    # Method to print freebie details
    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"