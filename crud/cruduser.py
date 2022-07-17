from sqlalchemy.orm import sessionmaker
from models import User
from models import UserLogs


class CrudUser():
    db: sessionmaker

    def __init__(self, db: sessionmaker):
        self.db = db

    def create(self, data: User):
        error = ""
        try:
            self.db.add(data)
        except Exception as xxx:
            error = str(xxx)
            print(error)
        return error

    def get_all(self, ten_id):
        userdata = self.db.query(User).filter(User.ten_id == ten_id)
        return userdata.all() if userdata else None

    def get_by_id(self, id: int):
        user = self.db.query(User).get(id)
        return user

    def get_by_username(self, username: str):
        user = None
        users = self.db.query(User).filter(User.username == username)
        if users:
            user = users.first()
        return user

    def add_user_log(self, user_id, action):
        log = UserLogs()
        log.user_id = user_id
        log.action_name = action
        self.db.add(log)

    def edit_user(self, data):
        dbuser = self.db.query(User).get(data["id"])
        if "username" in data:
            dbuser.username = data["username"]
        if "avatar" in data:
            dbuser.avatar = data["avatar"]
        if "fullname" in data:
            dbuser.fullname = data["fullname"]
        if "role" in data:
            dbuser.role = data["role"]
        if "status" in data:
            dbuser.status = data["status"]
        if "company" in data:
            dbuser.company = data["company"]
        if "email" in data:
            dbuser.email = data["email"]
        if "phone" in data:
            dbuser.phone = data["phone"]
        if "password_status" in data:
            dbuser.password_status = data["password_status"]
