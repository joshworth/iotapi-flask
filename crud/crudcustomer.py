from models import Customer, CustomerAccount, CustomerTransactions
from sqlalchemy.orm import sessionmaker, load_only


class CrudCustomer():
    db: sessionmaker

    def __init__(self, db: sessionmaker):
        self.db = db

    def create(self, data: Customer):
        self.db.add(data)
        return data

    def get_all(self, ten_id):
        custdata = self.db.query(Customer).filter(Customer.ten_id == ten_id)
        return custdata.all() if custdata else None

    def get_all_summary(self, ten_id):
        custdata = self.db.query(Customer).filter(Customer.ten_id == ten_id)
        return custdata.all() if custdata else None

    def get_by_id(self, id: int):
        custdata = self.db.query(Customer).get(id)
        return custdata

    def lookup_customer(self, ten_id, tag, account_no, customer_name, limit):
        output = None
        if tag == "account":
            output = self.db.query(
                Customer.id, Customer.customer_name, Customer.account_prefix,
                Customer.customer_type, Customer.primary_phone, Customer.ten_id).filter(Customer.ten_id == ten_id,
                                                                                        Customer.account_prefix.ilike(f'{account_no}%')).limit(limit)
        elif tag == "name":
            output = self.db.query(
                Customer.id, Customer.customer_name, Customer.account_prefix,
                Customer.customer_type, Customer.primary_phone, Customer.ten_id).filter(
                Customer.ten_id == ten_id, Customer.customer_name.ilike(f'%{customer_name}%')).limit(limit)
        return output.all() if output else None

    def edit(self, data):
        custdata: Customer = self.db.query(Customer).get(data["id"])
        custdata.fill(data)


class CrudCustomerAccount():
    db: sessionmaker

    def __init__(self, db: sessionmaker):
        self.db = db

    def create(self, data: CustomerAccount):
        self.db.add(data)
        return data

    def get_all(self, ten_id):
        custdata = self.db.query(CustomerAccount).filter(
            CustomerAccount.ten_id == ten_id)
        return custdata.all() if custdata else None

    def get_by_id(self, id: int):
        custdata = self.db.query(CustomerAccount).get(id)
        return custdata

    def get_by_account_no(self, ten_id: str, account_no: str):
        custdata = self.db.query(CustomerAccount).filter(
            CustomerAccount.account_no == account_no)
        return custdata.first() if custdata else None

    def get_by_device_id_active(self, device_id: int):
        devacc = None
        data = self.db.query(CustomerAccount).filter(
            CustomerAccount.device_id == device_id,
            CustomerAccount.status == "ACTIVE"
        )
        if data:
            devacc = data.first()
        return devacc

    def calculate_balance(self, ten_id, customer_account_id: int):
        # get acc transactions sorted by date
        tlist = CrudCustomerTransactions(
            self.db).get_account_transactions(ten_id, customer_account_id)
        balance = 0
        if tlist:
            for t in tlist:
                balance += t.balance if t.drcr == "CR" else -t.balance
        # build balance
        return balance

    def edit(self, data):
        custdata: CustomerAccount = self.db.query(
            CustomerAccount).get(data["id"])
        custdata.fill(data)


class CrudCustomerTransactions():
    db: sessionmaker

    def __init__(self, db: sessionmaker):
        self.db = db

    def create(self, data: CustomerTransactions):
        self.db.add(data)

    def get_all(self, ten_id):
        custdata = self.db.query(CustomerTransactions).filter(
            CustomerTransactions.ten_id == ten_id)
        return custdata

    def get_account_transactions(self, ten_id, acount_id):
        custdata = self.db.query(CustomerTransactions).filter(
            CustomerTransactions.ten_id == ten_id, CustomerTransactions.customer_account_id == acount_id).order_by(CustomerTransactions.date)
        return custdata

    def get_by_id(self, id: int):
        custdata = self.db.query(CustomerTransactions).get(id)
        return custdata

    def edit(self, data):
        custdata: CustomerTransactions = self.db.query(
            CustomerTransactions).get(data["id"])
        custdata.fill(data)
