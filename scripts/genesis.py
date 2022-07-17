import requests
import json
import sys
import time


class Genesis:
    end_point = 'http://127.0.0.1:50007'

    def __init__(self, mode):
        print("mode === {}".format(mode))
        if mode == "prod":
            self.end_point = 'http://127.0.0.1:5000/'
        elif mode == "test":
            #self.end_point = 'http://127.0.0.1:5000/'
            self.end_point = 'http://ec2-54-185-43-208.us-west-2.compute.amazonaws.com:8088/'

    def run(self):
        self.get_version()

        # setup first time user
        # self.create_super_admin()
        # self.create_guest_user()
        self.change_password()
        # self.create_settings()
        # self.create_alpha_tennant()

    def make_post(self, action, data):
        pdata = data
        url = f"{self.end_point}{action}"
        print("=============================================== calling : {}".format(url))
        post_results = requests.post(url, verify=False, json=pdata)
        print(post_results)
        print(post_results.text)

    def make_get(self, action):
        url = f"{self.end_point}{action}"
        print("=============================================== calling : {}".format(url))
        post_results = requests.get(url, verify=False)
        print(post_results)
        print(post_results.text)

    def get_version(self):
        url = f"{self.end_point}/version"
        print("============================================= calling : {}".format(url))
        post_results = requests.get(url, verify=False)
        print(post_results)
        data = post_results.text
        print(data)

    def create_super_admin(self):
        action = "signup"
        pdata = {
            "username": "admin@iotex.com",
            "fullname": "Administrator Tyrant",
            "password": "some cool password",
            "status": "active",
            "role": "admin",
        }
        self.make_post(action, pdata)

    def create_guest_user(self):
        action = "signup"
        pdata = {
            "username": "guest@iotex.com",
            "fullname": "Guest Tyrant",
            "password": "password",
            "status": "active",
            "role": "admin",
        }
        self.make_post(action, pdata)

    def change_password(self):
        action = "password/set"
        pdata = {
            "id": 2,
            "password": "password123",
            "password_status": "OPEN"
        }
        self.make_post(action, pdata)

    def create_alpha_tennant(self):
        action = "tennants/add"
        tennant = {
            "code": "101",
            "fullname": "Alpha Org",
            "email": "",
            "phone": ""
        }
        self.make_post(action, tennant)

    def create_settings(self):
        action = 'settings/add'
        # create
        items = []
        devtypes = {
            "runlevel": 1,
            "phrase": "Device Types",
            "detail": [
                {"code": "water_meter", "name": "Water Meter"},
                {"code": "sanitary_meter", "name": "Sanitary Meter"},
                {"code": "camera", "name": "Street Camera"},
                {"code": "gps", "name": "GPS Tracker"},
            ]}

        items.append(devtypes)

        log_schema = {
            "runlevel": 1, "phrase": "Log schema", "detail": {
                "water_meter": {"rows": [
                    {"name": "id", "type": "number", "text": "ID"},
                    {"name": "amount", "type": "number", "text": "Amount"},
                    {"name": "volume", "type": "number", "text": "Volume"},
                    {"name": "topup", "type": "number", "text": "Topup"},
                    {"name": "post_time", "type": "number", "text": "Posting Time"}
                ]
                },
                "sanitary_meter": {"rows": [
                    {"name": "id", "type": "number", "text": "ID"},
                    {"name": "amount", "type": "number", "text": "Amount"},
                    {"name": "event", "type": "string", "text": "Event"},
                    {"name": "duration", "type": "number", "text": "Duration"},
                    {"name": "post_time", "type": "number", "text": "Posting Time"}
                ]
                }
            }
        }
        items.append(log_schema)

        pdata = {"items": items}
        self.make_post(action, pdata)


def launch(params):
    nargs = len(params)
    if nargs < 2:
        print("ERROR: Insufficient number of commandline parameters.")
        return

    if params[1] == "prod" or params[1] == "test":
        test = Genesis(params[1])
        test.run()
    else:
        print("ERROR: Unknown commandline parameters {}".format(params[1]))
        return


launch(sys.argv)

# water_meter Water Meter

