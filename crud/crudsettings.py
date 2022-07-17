from sqlalchemy.orm import sessionmaker
from models import Settings, Tennants


class CrudSettings():
    db: sessionmaker

    def __init__(self, db: sessionmaker):
        self.db = db

    def create(self, data: Settings):
        self.db.add(data)

    def fetch(self, runlevel, ten_id):
        data = self.db.query(Settings).filter(
            Settings.runlevel <= runlevel, Settings.ten_id == ten_id)
        return data.all() if data else None

    def get_all(self, ten_id):
        data = self.db.query(Settings).filter(Settings.ten_id == ten_id)
        return data.all() if data else None

    def get_by_id(self, id: int):
        setting = self.db.query(Settings).get(id)
        return setting

    def edit_setting(self, data):
        dbsetting = self.db.query(Settings).get(data["id"])
        if "phrase" in data:
            dbsetting.phrase = data["phrase"]
        if "detail" in data:
            dbsetting.detail = data["detail"]
        if "runlevel" in data:
            dbsetting.runlevel = data["runlevel"]


class CrudTennants():
    db: sessionmaker

    def __init__(self, db: sessionmaker):
        self.db = db

    def create(self, data: Tennants):
        self.db.add(data)

    def get_all(self):
        data = self.db.query(Tennants).all()
        return data

    def get_by_id(self, id: int):
        data = self.db.query(Tennants).get(id)
        return data

    def edit_setting(self, data):
        dbsetting = self.db.query(Settings).get(data["id"])
        if "phrase" in data:
            dbsetting.phrase = data["phrase"]
        if "detail" in data:
            dbsetting.detail = data["detail"]
        if "runlevel" in data:
            dbsetting.runlevel = data["runlevel"]
