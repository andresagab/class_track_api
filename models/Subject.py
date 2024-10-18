from config.database import Base
from sqlalchemy import Column, Integer, String

class Subject(Base):
    # define the table name
    __tablename__ = "subjects"

    # define the properties of model
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), unique=True)
    description = Column(String(300), nullable=True)