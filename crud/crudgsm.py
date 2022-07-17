from models import GsmPost
from sqlalchemy.orm import sessionmaker


class CrudGsmPost:
    db: sessionmaker

    def __init__(self, db: sessionmaker):
        self.db = db

    def create(self, data: GsmPost):
        error = ""
        try:
            self.db.add(data)
        except Exception as xxx:
            error = str(xxx)
            print(error)
        return error

    def getAll(self):
        gsmdata = self.db.query(GsmPost).all()
        return gsmdata

    def getById(self, id: int):
        user = self.db.query(GsmPost).get(id)
        return user
