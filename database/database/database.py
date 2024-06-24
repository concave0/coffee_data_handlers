from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime


# SQLite Database Connection
engine = create_engine('sqlite:///database/coffeedata.db', echo=True) # 'echo=True' logs SQL queries
Base = declarative_base()

# Define 'User' Model
class CoffeeData(Base):
    __tablename__ = 'coffee_data'

    id = Column(Integer, primary_key=True, index=True) 
    name = Column(String, nullable=False)
    facts = Column(String, unique=True, index=True)
    commit_date = Column(String)

# Create Tables (if not exists)
Base.metadata.create_all(bind=engine)

# Session Setup
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Interaction with Database
def create_new_coffee(id:int, name:str, facts:str, commit_date:str):
    try: 
        with SessionLocal() as session:
            new_coffee = CoffeeData(id=id, name=name, facts=facts , commit_date= commit_date)
            session.add(new_coffee)
            session.commit()
            session.refresh(new_coffee)
            return new_coffee , True
    except:
        return False 
    

def get_all_coffee():
    with SessionLocal() as session:
        coffee = session.query(CoffeeData).all()
        return coffee
    
# Querying for a Specific Coffee
def get_specfic_coffee_details(id:int):
    with SessionLocal() as session:
        coffee = session.get(CoffeeData, id)
        return coffee
