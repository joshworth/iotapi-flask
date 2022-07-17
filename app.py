import flask
from flask import Flask, request, jsonify, make_response
import json
import datetime

# from flask_jwt_extended import jwt_refresh_token_required
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import jwt
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_cors import CORS
from services import UserService, GsmService, DeviceService, SettingsService, CustomerService, UtilityService
from database import Session

import os
from flask import flash, redirect, url_for
from werkzeug.utils import secure_filename


db_session = Session()

iotapp = flask.Flask(__name__)
CORS(iotapp)

iotapp.config["DEBUG"] = False
iotapp.config["JSON_SORT_KEYS"] = False
iotapp.config["SECRET_KEY"] = "your secret key"
iotapp.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
iotapp.config["JWT_IDENTITY_CLAIM"] = "username"
iotapp.config["PROPAGATE_EXCEPTIONS"] = True
iotapp.config["UPLOAD_FOLDER"] = "data/files"
iotapp.config["TEMP_FOLDER"] = "data/temp"

jwt_manager = JWTManager(iotapp)


version_data = {"version": 0, "lastaccess": 0, "name": "data agent", "time": datetime.now()}

# SECTION: Heart beat =========================================================


@iotapp.route("/", methods=["GET"])
def home():
    return "<h1>IT Works - IoT API</h1><p>Yes it works!!!</p>"


@iotapp.route("/version", methods=["GET"])
def version():
    version_data["version"] = version_data["version"] + 1
    version_data["lastaccess"] = version_data["lastaccess"] + 3
    version_data["time"] = datetime.now()

    # message = f'<h1>Test Get</h1><p>Version: {data["version"]}, <br>Accessed: {data["lastaccess"]}, <br>Name: {data["name"]}, <br>Data: {str(data)} </p>'

    return jsonify(version_data)


# SECTION: User Auth =========================================================


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # jwt is passed in the request header
        jwt_token = request.headers.get("Authorization", None)
        print(jwt_token)
        if jwt_token:
            try:
                jwt_token = jwt_token.replace("Bearer ", "").strip()
                print(jwt_token)
                # decoding the payload to fetch the stored details
                data = jwt.decode(jwt_token, iotapp.config["SECRET_KEY"])
                current_user = UserService().get_user_login(db_session, data["username"])
            except Exception as ex:
                print(str(ex))
                return jsonify({"message": "Token is invalid !!"}), 401
        else:
            return jsonify({"message": "Token is missing !!"}), 401

        # returns the current logged in users contex to the routes
        return f(current_user, *args, **kwargs)

    return decorated


@iotapp.route("/list-users", methods=["POST"])
def api_list_users():
    data = request.json
    service = UserService()
    user_list = service.list_users_summary(db=db_session, ten_id=data["ten_id"])
    result = {"error": "", "data": user_list}
    print("return result ==================== ")
    print(result)

    return jsonify(result)


# User Database Route
# this route sends back list of users users
@iotapp.route("/user", methods=["GET"])
@token_required
def get_all_users(current_user):
    data = request.json
    # querying the database
    # for all the entries in it
    users = UserService().list_user_objects(db_session, data["ten_id"])
    # converting the query objects
    # to list of jsons
    output = []
    for user in users:
        # appending the user data json
        # to the response list
        output.append(
            {
                "id": user.id,
                "username": user.username,
                "fullname": user.fullname,
                "email": user.email,
                "role": user.role,
                "status": user.status,
            }
        )

    return jsonify({"users": output})


@iotapp.route("/refresh-token", methods=["POST"])
# @jwt_refresh_token_required
def refresh_token():
    print("<<<< === refresh_token =============================== >>>>> ")
    # retrive the user's identity from the refresh token using a Flask-JWT-Extended built-in method
    current_user = get_jwt_identity()
    # return a non-fresh token for the user
    new_token = create_access_token(identity=current_user, fresh=False)
    return {"accessToken": new_token}, 200


# route for loging user in
@iotapp.route("/login", methods=["POST"])
def login():
    # creates dictionary of form data
    auth = request.json

    login_response = UserService().login_user(db_session, iotapp.config["SECRET_KEY"], auth)
    return login_response


# signup route


@iotapp.route("/signup", methods=["POST"])
def signup():
    # creates a dictionary of the form data
    data = request.json
    response = UserService().signup_user(db_session, data)
    return jsonify(response)


@iotapp.route("/signup/customer", methods=["POST"])
def signup_customer():
    # creates a dictionary of the form data
    data = request.json
    response = UserService().signup_user_from_customer(db_session, data)
    return jsonify(response)


@iotapp.route("/password/set", methods=["POST"])
def password_set():
    # creates a dictionary of the form data
    data = request.json
    print(data)
    response = UserService().set_password(db_session, data)
    return jsonify(response)


@iotapp.route("/fetch-user", methods=["POST"])
def fetch_user():
    # creates a dictionary of the form data
    data = request.json
    print("=============================== fetch_user ======================== data ", data)
    id = data["id"]
    print("=============================== fetch_user ======================== id ", id)

    response = UserService().get_user(db_session, id)
    print("=============================== fetch_user ==", response)
    return jsonify(response)


@iotapp.route("/edit-user", methods=["POST"])
def edit_user():
    # creates a dictionary of the form data
    data = request.json
    response = UserService().edit_user(db_session, data)
    return jsonify(response)


# SECTION: Device =========================================================


@iotapp.route("/device/add", methods=["POST"])
def device_add():
    # creates a dictionary of the form data
    data = request.json
    response = DeviceService().add_device(db_session, data)
    return jsonify(response)


@iotapp.route("/device/edit", methods=["POST"])
def device_edit():
    # creates a dictionary of the form data
    data = request.json
    response = DeviceService().edit_device(db_session, data)
    return jsonify(response)


@iotapp.route("/device/list", methods=["POST"])
def device_list():
    data = request.json
    response = DeviceService().list_devices_summary(db_session, data["ten_id"])
    return jsonify(response)


@iotapp.route("/device/get-one", methods=["POST"])
def device_fetch():
    data = request.json
    response = DeviceService().get_device(db_session, data["id"])
    return jsonify(response)


@iotapp.route("/device/log", methods=["POST"])
def device_log():
    data = request.json
    response = DeviceService().post_device_log(db_session, data)
    return jsonify(response)


# SECTION: Customer =========================================================
@iotapp.route("/customer/add", methods=["POST"])
def customer_add():
    data = request.json
    response = CustomerService().add_customer(db_session, data)
    return jsonify(response)


@iotapp.route("/customer/edit", methods=["POST"])
def customer_edit():
    data = request.json
    response = CustomerService().add_customer(db_session, data)
    return jsonify(response)


@iotapp.route("/customer/list", methods=["POST"])
def customer_list():
    data = request.json
    response = CustomerService().list_customers(db_session, data["ten_id"])
    return jsonify(response)


@iotapp.route("/customer/list-summary", methods=["POST"])
def customer_list_summary():
    data = request.json
    response = CustomerService().list_customers_summary(db_session, data["ten_id"])
    return jsonify(response)


@iotapp.route("/customer/lookup", methods=["POST"])
def customer_lookup():
    data = request.json
    response = CustomerService().lookup_customer(db_session, data)
    return jsonify(response)


@iotapp.route("/customer/get-one", methods=["POST"])
def customer_get_one():
    data = request.json
    response = CustomerService().get_customer(db_session, data["id"])
    return jsonify(response)


@iotapp.route("/customer/add-trans", methods=["POST"])
def customer_add_transaction():
    data = request.json
    response = CustomerService().add_customer_transaction(db_session, data)
    return jsonify(response)


@iotapp.route("/customer/add-group-trans", methods=["POST"])
def customer_add_group_transaction():
    data = request.json
    response = CustomerService().add_group_transaction(db_session, data)
    return jsonify(response)


# SECTION: Settings =========================================================


@iotapp.route("/settings/add", methods=["POST"])
def settings_add():
    data = request.json
    response = SettingsService().add_settings(db_session, data)
    return jsonify(response)


@iotapp.route("/settings/edit", methods=["POST"])
def settings_edit():
    data = request.json
    response = SettingsService().edit_setting(db_session, data)
    return jsonify(response)


@iotapp.route("/settings/fetch", methods=["POST"])
def settings_fetch():
    data = request.json
    response = SettingsService().fetch_settings(db_session, data["ten_id"], data["runlevel"])
    return jsonify(response)


@iotapp.route("/tennants/add", methods=["POST"])
def tennants_add():
    data = request.json
    response = SettingsService().add_tennant(db_session, data)
    return jsonify(response)


@iotapp.route("/device/format-detail", methods=["GET"])
def device_detail_format():
    result = DeviceService().format_detail(db_session, 1)
    return jsonify(result)


@iotapp.route("/upload_file", methods=["POST"])
def upload_file():
    result = {"error": "", "data": ""}
    error = UtilityService().upload_file(iotapp.config["UPLOAD_FOLDER"], request)
    if len(error) == 0:
        result["data"] = "Success"
    else:
        result["error"] = error
    return result


@iotapp.route("/import/data", methods=["POST"])
def import_data():
    result = {"error": "", "data": ""}
    result = UtilityService().upload_template_data(db_session, request)
    return result


if __name__ == "__main__":
    # import logging
    # logging.basicConfig(filename='error.log', level=logging.DEBUG)
    iotapp.run(debug=True)
