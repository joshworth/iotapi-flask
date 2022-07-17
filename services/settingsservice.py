from models import Settings, Tennants
from crud import CrudSettings, CrudTennants
from sqlalchemy.orm import sessionmaker
import json
from .utils import process_exception


class SettingsService:
    def add_settings(self, db: sessionmaker, data):
        result = {"error": "", "data": ""}
        try:
            print("========================================== data", data)
            # we expect an array of settings
            for item in data["items"]:
                newset = Settings()
                # convert to json string
                item["detail"] = json.dumps(item["detail"])
                newset.fill(item)
                print("========================================== new dev ", newset)
                CrudSettings(db).create(newset)
            db.commit()
            result["data"] = "Success"
        except Exception as xxx:
            error = process_exception(xxx)
            result["error"] = error
            db.rollback()
        return result

    def edit_setting(self, db: sessionmaker, data):
        result = {"error": "", "data": ""}
        try:
            data["detail"] = json.dumps(data["detail"])
            CrudSettings(db).edit_setting(data)
            db.commit()
            result = {"error": "", "data": "Success"}
        except Exception as xxx:
            error = process_exception(xxx)
            result["error"] = error
            db.rollback()
        return result

    def fetch_settings(self, db: sessionmaker, ten_id, runlevel):
        result = {"error": "", "data": {}}
        try:
            setlist = CrudSettings(db).fetch(runlevel, ten_id)
            # create dictionary from settings
            for sett in setlist:
                dset = sett.to_dict()
                print("adding: =====", dset)
                key = dset["phrase"]
                dset["detail"] = json.loads(dset["detail"])
                result["data"][key] = dset
        except Exception as xxx:
            error = process_exception(xxx)
            result["error"] = error
            db.rollback()
        return result

    # ================================== tennants
    def add_tennant(self, db: sessionmaker, data):
        result = {"error": "", "data": {}}
        try:
            tennant: Tennants = Tennants()
            tennant.fill(data)
            CrudTennants(db).create(tennant)
            db.commit()
            result["data"] = "Success"
        except Exception as xxx:
            error = process_exception(xxx)
            result["error"] = error
            db.rollback()
        return result

    def update_config(self, db: sessionmaker, data):
        result = {"error": "", "data": {}}
        try:
            tennant: Tennants = CrudTennants(db).get_by_id(data["tenant_id"])
            if tennant:
                tennant.detail = data
                db.commit()
            else:
                result["error"] = "ERROR: Tennant not found."
            result["data"] = "Success"
        except Exception as xxx:
            error = process_exception(xxx)
            result["error"] = error
            db.rollback()
        return result

    def fetch_tennant(self, db: sessionmaker, id: int):
        result = {"error": "", "data": {}}
        try:
            tennant: Tennants = CrudTennants(db).get_by_id(id)
            if tennant:
                result["data"] = tennant.to_dict()
            else:
                result["error"] = "ERROR: Tennant not found."
        except Exception as xxx:
            error = process_exception(xxx)
            result["error"] = error
            db.rollback()
        return result
