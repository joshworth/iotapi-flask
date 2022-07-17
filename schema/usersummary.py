class UserSummary:
    id: int
    username: str
    fullname: str
    role: str
    status: str
    last_activity: str

    def __init__(self, userid: int, username: str, fullname: str, role: str, status: str):
        self.id = userid
        self.username = username
        self.fullname = fullname
        self.role = role
        self.status = status
        self.last_activity = ""

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "fullname": self.fullname,
            "role": self.role,
            "status": self.status,
            "last_activity": self.last_activity
        }
