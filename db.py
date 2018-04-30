from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, validates

# start database engine
db_uri = 'sqlite:////Users/alexloyko/Desktop/RestaurantInspections.db'
engine = create_engine(db_uri)

Base = declarative_base()
DBsession = sessionmaker(bind=engine)

# restaurant model
class Restaurant(Base):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String)
    boro = Column(String)
    building = Column(String)
    street = Column(String)
    zip = Column(Integer)
    phone = Column(String)
    cuisine = Column(String)

    @validates('name', 'boro', 'building', 'street', 'phone', 'cuisine')
    def convert_upper(self, key, value):
        value = str(value)
        return value.upper()

# inspection model
class Inspection(Base):
    __tablename__ = 'inspections'
    id = Column(Integer, primary_key=True)
    rest_id = Column(Integer, ForeignKey(Restaurant.id))
    inspection_date = Column(Date)
    action = Column(String)
    violation_code = Column(String)
    violation_desc = Column(String)
    is_critical = Column(Boolean)
    score = Column(Integer)
    grade = Column(String)
    grade_date = Column(Date)
    record_date = Column(Date)
    inspection_type = Column(String)

# create tables from models
Base.metadata.bind = engine
Base.metadata.create_all()
