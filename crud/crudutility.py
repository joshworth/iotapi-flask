from sqlalchemy.orm import sessionmaker
from models import ImportLogs


class CrudImportlogs():
    db: sessionmaker

    def __init__(self, db: sessionmaker):
        self.db = db

    def create(self, data: ImportLogs):
        self.db.add(data)

    def get_all(self):
        data = self.db.query(ImportLogs).all()
        return data

    def get_by_id(self, id: int):
        data = self.db.query(ImportLogs).get(id)
        return data

    def get_by_name(self, ten_id, name: str):
        data = self.db.query(ImportLogs).filter(
            ImportLogs.ten_id == ten_id, ImportLogs.file_id == name)
        return data.first() if data else None
