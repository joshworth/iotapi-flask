from sqlalchemy.orm import sessionmaker
from models import Device, DeviceLogs


class CrudDevice():
    db: sessionmaker

    def __init__(self, db: sessionmaker):
        self.db = db

    def create(self, data: Device):
        self.db.add(data)

    def get_all(self, ten_id):
        devdata = self.db.query(Device).filter(Device.ten_id == ten_id)
        return devdata.all() if devdata else None

    def get_by_id(self, id: int):
        dev = self.db.query(Device).get(id)
        return dev

    def get_by_barcode(self, ten_id, barcode: str):
        dev = None
        devq = self.db.query(Device).filter(
            Device.barcode == barcode, Device.ten_id == ten_id)
        if devq:
            dev = devq.first()
        return dev

    def edit_device(self, data):
        dev = self.db.query(Device).get(data["id"])
        if "serial_number" in data:
            dev.serial_number = data["serial_number"]
        if "device_type" in data:
            dev.device_type = data["device_type"]
        if "barcode" in data:
            dev.barcode = data["barcode"]

    def create_device_log(self, data: DeviceLogs):
        self.db.add(data)

    def get_device_logs(self, ten_id, device_id):
        devdata = self.db.query(DeviceLogs).filter(
            DeviceLogs.device_id == device_id, DeviceLogs.ten_id == ten_id)
        return devdata.all() if devdata else None

    def get_device_logs_all(self, ten_id):
        devdata = self.db.query(DeviceLogs).filter(DeviceLogs.ten_id == ten_id)
        return devdata.all() if devdata else None
