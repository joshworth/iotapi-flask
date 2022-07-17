from sqlalchemy.orm import sessionmaker
from models import User, UserLogs, Customer
from crud import CrudUser, CrudCustomer, CrudSettings, CrudTennants
from schema import UserSummary
from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, create_refresh_token,
    get_jwt_identity
)
import sys
from .utils import process_exception


class UserService:
    def login_user(self, db: sessionmaker, secret_key, auth):
        try:
            if not auth or not auth['username'] or not auth['password']:
                # returns 401 if any email or / and password is missing
                return make_response(
                    'Could not verify',
                    401,
                    {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
                )

            username = auth.get('username')
            user = UserService().get_user_login(db=db, username=username)

            if not user:
                # returns 401 if user does not exist
                print("error, user status ============= no user")
                return make_response(
                    'Could not verify',
                    402,
                    {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
                )

            if check_password_hash(user.password, auth.get('password')):
                # user should be active
                if user.status != "ACTIVE":
                    print("error, user status ============= ",
                          user.status, user.status)
                    # returns 401 if user does not exist
                    return make_response(
                        'Could not verify',
                        407,
                        {'WWW-Authenticate': 'Basic realm ="User is not active !!"'}
                    )

                print("============== user ", user.to_dict())
                # fetch tennant info
                tdata = CrudTennants(db).get_by_id(user.ten_id)
                print("============== tdata ", tdata.to_dict())

                # generates the JWT Token
                token = jwt.encode(
                    {
                        'id': user.id,
                        'username': user.username,
                        'fullname': user.fullname,
                        'ten_id': tdata.id,
                        'ten_name': tdata.fullname,
                        'role': user.role,
                        'password_status': user.password_status,
                        'exp': datetime.utcnow() + timedelta(minutes=30)},
                    secret_key
                )
                ref_token = create_refresh_token(identity=user.username)

                UserService().log_user_activity(db, user.id, "LOGIN")
                print('===============', ref_token)

                # take care of decode on version issues
                ispy37 = sys.version.startswith("3.7")
                access_token = token.decode() if ispy37 else token

                return make_response(jsonify(
                    {
                        'accessToken': access_token,
                        'refreshToken': ref_token
                    }
                ), 201)

            # returns 403 if password is wrong
            print("error, user status ============= wrong password")
            return make_response(
                'Could not verify',
                409,
                {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
            )
        except Exception as xxx:
            print("gen error, user status ============= ", str(xxx))
            return make_response(
                'General API Error',
                405,
                {'WWW-Authenticate': 'Application Error"'}
            )

    def create_user(self, db: sessionmaker, data):
        error = ""
        username = data['username']
        password = data["password"]
        # checking for existing user
        new_user: User = None
        user = self.get_user_login(db, username)
        if not user:
            # database ORM object
            data["password"] = generate_password_hash(password)
            new_user = User()
            new_user.fill(data)
            print("========================>> ", new_user.as_dict())
            error = CrudUser(db).create(new_user)
            if error == "":
                db.commit()
            else:
                print("error:: ", error)
                error = "General error."
        else:
            error = f"User already exists. [{username}]"

        return error, new_user

    def signup_user(self, db: sessionmaker, data):
        result = {
            "error": "",
            "data": ""
        }
        try:
            error, new_user = self.create_user(db, data)
            if len(error) == 0:
                result["data"] = "Success"
            else:
                result["error"] = error
        except Exception as xxx:
            error = process_exception(xxx)
            result["error"] = error
            db.rollback()
        return result

    def signup_user_from_customer(self, db: sessionmaker, data):
        result = {
            "error": "",
            "data": ""
        }
        try:
            error, new_user = self.create_user(db, data)
            if len(error) == 0:
                # now update customer
                cid = data["customer_id"]
                customer: Customer = CrudCustomer(db).get_by_id(cid)
                if customer:
                    customer.user_id = new_user.id
                    db.commit()
                    result["data"] = "Success"
                else:
                    result["error"] = f"ERROR: Customer not found for ID {cid}"
            else:
                result["error"] = error
        except Exception as xxx:
            error = process_exception(xxx)
            result["error"] = error
            db.rollback()

        return result

    def set_password(self, db: sessionmaker, data):
        id = data['id']
        new_password = data["password"]
        # checking for existing user
        user = CrudUser(db).get_by_id(id)
        password = generate_password_hash(new_password)
        result = {
            "error": "",
            "data": ""
        }
        user.password = password
        user.password_status = data["password_status"]
        db.commit()

        return result

    def edit_user(self, db: sessionmaker, data):
        CrudUser(db).edit_user(data)
        db.commit()
        result = {
            "error": "",
            "data": "Success"
        }
        return result

    def get_user(self, db: sessionmaker, id: int):
        login_user = CrudUser(db).get_by_id(id)
        #result = login_user.as_dict() if login_user else None
        result = {
            "error": "",
            "data": ""
        }
        if login_user:
            result["data"] = login_user.to_dict()
        else:
            result["error"] = "Specified user does not exist".capitalize
        return result

    def get_user_login(self, db: sessionmaker, username):
        login_user = CrudUser(db).get_by_username(username)
        return login_user

    def list_users_summary(self, db: sessionmaker, ten_id: int):
        users_list = CrudUser(db).get_all(ten_id)
        result = []
        for user in users_list:
            duser = UserSummary(user.id, user.username,
                                user.fullname, user.role, user.status).to_dict()
            if len(user.user_logs) > 0:
                last_act = user.user_logs[len(user.user_logs)-1]
                duser["last_activity"] = last_act.action_time.strftime(
                    "%m/%d/%Y, %H:%M:%S")
            result.append(duser)
        return result

    def list_users(self, db: sessionmaker, ten_id: int):
        users_list = CrudUser(db).get_all(ten_id)
        result = []
        for user in users_list:
            duser = user.to_dict()
            acts = []
            for log in user.user_logs:
                acts.append(log.to_dict())
            duser["user_logs"] = acts

            result.append(duser)
        return result

    def list_user_objects(self, db: sessionmaker, ten_id: int):
        users_list = CrudUser(db).get_all(ten_id)
        return users_list

    def log_user_activity(self, db: sessionmaker, user_id: int, action: str):
        CrudUser(db).add_user_log(user_id, action)
        db.commit()
