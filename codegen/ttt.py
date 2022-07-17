from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey, Table, Column, Integer, Float, String, Boolean, UniqueConstraint, Numeric, DateTime, UniqueConstraint

Base = declarative_base()


class Employee(Base, SerializerMixin):
    __tablename__ = "emp"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    age = Column(String)
    salary = Column(Integer)
    country = Column(String)
    serialize_only = ("id", "name", "address", "age", "salary", "country")

    def __init__(
        self,
    ):
        print("init............")

    def fill(self, _dict):
        self.__dict__.update(_dict)
        print("self ... ", self)
        print("dict ... ", self.to_dict())


emp = Employee()
data = {"id": 100, "name": "wase", "age": 30}
emp.fill(data)
data = {"country": "ug", "age": 39}
emp.fill(data)
