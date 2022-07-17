from crud import CrudDevice
from models import Device, DeviceLogs
from sqlalchemy.orm import sessionmaker
from .utils import process_exception
import json


class DeviceService:
    def add_device(self, db: sessionmaker, data):
        result = {"error": "", "data": ""}
        try:
            print("========================================== data", data)
            newdev = Device()
            newdev.fill(data)
            print("========================================== new dev ", newdev)
            CrudDevice(db).create(newdev)
            db.commit()
            result["data"] = "Success"
        except Exception as xxx:
            error = process_exception(xxx)
            result["error"] = error
            db.rollback()
        return result

    def list_devices_summary(self, db: sessionmaker, ten_id: int):
        result = {"error": "", "data": []}
        try:
            dev_list = CrudDevice(db).get_all(ten_id)
            for dev in dev_list:
                pdev = dev.to_dict()
                nlogs = len(dev.device_logs)
                last_log = ""
                if nlogs > 0:
                    log = dev.device_logs[nlogs - 1]
                    last_log = log.post_time.strftime("%m/%d/%Y, %H:%M:%S")
                pdev["log_activity"] = nlogs
                pdev["last_activity"] = last_log

                result["data"].append(pdev)
        except Exception as xxx:
            error = process_exception(xxx)
            result["error"] = error
            db.rollback()
        return result

    def get_device(self, db: sessionmaker, id):
        dev: Device = CrudDevice(db).get_by_id(id)
        result = {"error": "", "data": ""}
        try:
            if dev:
                retdev = dev.to_dict()
                # add account details
                retdev["account_no"] = ""
                retdev["account_name"] = ""
                # import pdb  pdb.set_trace()
                if dev.customer_account:
                    retdev["account_no"] = dev.customer_account[0].account_no
                    retdev["account_name"] = dev.customer_account[0].customer.customer_name

                logs = []
                for log in dev.device_logs:
                    dlog = {}
                    dlog["id"] = log.id
                    dlog["post_time"] = log.post_time.strftime("%m/%d/%Y, %H:%M:%S")
                    dlog["detail"] = json.loads(log.detail)
                    logs.append(dlog)
                retdev["logs"] = logs
                result["data"] = retdev

            else:
                result["error"] = "Specified device does not exist"
        except Exception as xxx:
            print("error =========== ", str(xxx))
            error = process_exception(xxx)
            result["error"] = error
            db.rollback()

        return result

    def get_device_by_barcode(self, db: sessionmaker, barcode, ten_id):
        dev = CrudDevice(db).get_by_barcode(barcode, ten_id)
        result = {"error": "", "data": ""}
        try:
            if dev:
                retdev = dev.to_dict()
                logs = []
                for log in dev.device_logs:
                    dlog = {}
                    dlog["id"] = log.id
                    dlog["post_time"] = log.post_time.strftime("%m/%d/%Y, %H:%M:%S")
                    dlog["detail"] = json.loads(log.detail)
                    logs.append(dlog)
                retdev["logs"] = logs
                result["data"] = retdev

            else:
                result["error"] = "Specified device does not exist"
        except Exception as xxx:
            print("error =========== ", str(xxx))
            error = process_exception(xxx)
            result["error"] = error
            db.rollback()

        return result

    def edit_device(self, db: sessionmaker, data):
        result = {"error": "", "data": ""}
        try:
            print("edit_device ============== ", data)
            CrudDevice(db).edit_device(data)
            db.commit()
            result["data"] = "Success"
        except Exception as xxx:
            error = process_exception(xxx)
            result["error"] = error
            db.rollback()
        return result

    def post_device_log(self, db: sessionmaker, data):
        result = {"error": "", "data": ""}
        try:
            print("========================================== data", data)
            devlog = DeviceLogs()
            data["detail"] = json.dumps(data)
            devlog.fill(data)
            print("========================================== new dev log ", devlog)
            CrudDevice(db).create_device_log(devlog)
            db.commit()
            result["data"] = "Success"
        except Exception as xxx:
            error = process_exception(xxx)
            result["error"] = error
            db.rollback()
        return result

    def format_detail(self, db: sessionmaker, ten_id):
        result = {"error": "", "data": {}}
        try:
            log_list = CrudDevice(db).get_device_logs_all(ten_id)
            # create dictionary from settings
            found = 0
            for log in log_list:
                lg = log.to_dict()
                print(f"log ................ {log.device.device_type}-{lg}")
                if log.device.device_type == "Water Meter" and not log.detail:
                    detail = {"device_id": log.device_id, "amount": str(round(log.amount, 2)) if log.amount else "0", "volume": str(round(log.volume, 2)) if log.volume else "0", "topup": str(round(log.topup, 2)) if log.topup else "0"}
                    log.detail = json.dumps(detail)
                    db.commit()
                    found += 1
                    print(f"Found ................ {found}")
            result["data"] = f"Sucess: Updated - {found}"
        except Exception as xxx:
            error = process_exception(xxx)
            result["error"] = error
            db.rollback()
        return result
