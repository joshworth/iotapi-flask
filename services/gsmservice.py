from models import GsmPost
from crud import CrudGsmPost
from sqlalchemy.orm import sessionmaker


class GsmService:
    def post_gsm(self, db: sessionmaker, data):
        gsmpost = GsmPost(
            device_id=data['device_id'],
            amount=data['amount'],
            volume=data['volume'],
            topup=data['topup']
        )
        error = CrudGsmPost(db).create(gsmpost)
        if error == "":
            print("comitting changes ================")
            db.commit()

        return error

    def list_gsm(self, db: sessionmaker):
        gsm_list = CrudGsmPost(db).getAll()
        result = []
        for gsm in gsm_list:
            result.append(gsm.serialize())
        return result
