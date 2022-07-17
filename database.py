from models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
import yaml


def load_db_conf():
    print("Loading app config .... ")
    data = None
    with open("conf/app.yaml", "r") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    print("... Done Loading app config")
    return data


"""
# pg_db_engine = create_engine("postgres://postgres:admin@localhost:5432/iot_db", echo=True)
dbuser = 'postgres'
db = 'iot_db'
dbpass = parse.unquote_plus('admin')
engine = create_engine(f'postgres://{dbuser}:{dbpass}@localhost:5432/{db}')
Session = sessionmaker(bind=engine)
"""

app_conf = load_db_conf()
pg = app_conf["database"]["postgres"]

print("Creating session ...")
# pg_db_engine = create_engine("postgres://postgres:admin@localhost:5432/iot_db", echo=True)
dbuser = pg["user"]
db = pg["db"]
dbpass = pg["password"]
engine = create_engine(f"postgresql://{dbuser}:{dbpass}@localhost:5432/{db}")
Session = sessionmaker(bind=engine)

print("... done creating session")
Base.metadata.create_all(engine)