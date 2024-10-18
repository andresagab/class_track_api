import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

# set path of sqllite file
sqilte_file = "../database.sqlite"
# define base dir with path of current file
base_dir = os.path.dirname(os.path.realpath(__file__))
# define URL of database connection
database_url = f"sqlite:///{os.path.join(base_dir, sqilte_file)}"
# define engine
engine = create_engine(database_url, echo=True)
# define Session
Session = sessionmaker(bind = engine)
# define base to manage database
Base = declarative_base()