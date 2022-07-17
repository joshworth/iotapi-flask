
from sqlalchemy.orm import sessionmaker, load_only
from models import User, UserLogs

class _CrudUser():
   db: sessionmaker

   def __init__(self, db: sessionmaker):
      self.db = db

   def create(self, data: User):
      self.db.add(data)
      return data

   def edit(self, data):
      user_data: User = self.db.query(User).get(data["id"])
      if user_data:
         user_data.fill(data)
      return user_data

   def get_all(self, ten_id):
      user_data = self.db.query(User).filter(User.ten_id == ten_id)
      return user_data.all() if user_data else None

   def get_by_id(self, user_id: int):
      user_data = self.db.query(User).get(user_id)
      return user_data


class _CrudUserLogs():
   db: sessionmaker

   def __init__(self, db: sessionmaker):
      self.db = db

   def create(self, data: UserLogs):
      self.db.add(data)
      return data

   def edit(self, data):
      user_logs_data: UserLogs = self.db.query(UserLogs).get(data["id"])
      if user_logs_data:
         user_logs_data.fill(data)
      return user_logs_data

   def get_all(self, ten_id):
      user_logs_data = self.db.query(UserLogs).filter(UserLogs.ten_id == ten_id)
      return user_logs_data.all() if user_logs_data else None

   def get_by_id(self, user_logs_id: int):
      user_logs_data = self.db.query(UserLogs).get(user_logs_id)
      return user_logs_data

