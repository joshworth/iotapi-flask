
from sqlalchemy.orm import sessionmaker, load_only
from models import LoanProduct, LoanApplication, Guarantee, LoanHistory, LoanSchedule, LoanTransactions

class _CrudLoanProduct():
   db: sessionmaker

   def __init__(self, db: sessionmaker):
      self.db = db

   def create(self, data: LoanProduct):
      self.db.add(data)
      return data

   def edit(self, data):
      loan_product_data: LoanProduct = self.db.query(LoanProduct).get(data["id"])
      if loan_product_data:
         loan_product_data.fill(data)
      return loan_product_data

   def get_all(self, ten_id):
      loan_product_data = self.db.query(LoanProduct).filter(LoanProduct.ten_id == ten_id)
      return loan_product_data.all() if loan_product_data else None

   def get_by_id(self, loan_product_id: int):
      loan_product_data = self.db.query(LoanProduct).get(loan_product_id)
      return loan_product_data


class _CrudLoanApplication():
   db: sessionmaker

   def __init__(self, db: sessionmaker):
      self.db = db

   def create(self, data: LoanApplication):
      self.db.add(data)
      return data

   def edit(self, data):
      loan_application_data: LoanApplication = self.db.query(LoanApplication).get(data["id"])
      if loan_application_data:
         loan_application_data.fill(data)
      return loan_application_data

   def get_all(self, ten_id):
      loan_application_data = self.db.query(LoanApplication).filter(LoanApplication.ten_id == ten_id)
      return loan_application_data.all() if loan_application_data else None

   def get_by_id(self, loan_application_id: int):
      loan_application_data = self.db.query(LoanApplication).get(loan_application_id)
      return loan_application_data


class _CrudGuarantee():
   db: sessionmaker

   def __init__(self, db: sessionmaker):
      self.db = db

   def create(self, data: Guarantee):
      self.db.add(data)
      return data

   def edit(self, data):
      guarantee_data: Guarantee = self.db.query(Guarantee).get(data["id"])
      if guarantee_data:
         guarantee_data.fill(data)
      return guarantee_data

   def get_all(self, ten_id):
      guarantee_data = self.db.query(Guarantee).filter(Guarantee.ten_id == ten_id)
      return guarantee_data.all() if guarantee_data else None

   def get_by_id(self, guarantee_id: int):
      guarantee_data = self.db.query(Guarantee).get(guarantee_id)
      return guarantee_data


class _CrudLoanHistory():
   db: sessionmaker

   def __init__(self, db: sessionmaker):
      self.db = db

   def create(self, data: LoanHistory):
      self.db.add(data)
      return data

   def edit(self, data):
      loan_history_data: LoanHistory = self.db.query(LoanHistory).get(data["id"])
      if loan_history_data:
         loan_history_data.fill(data)
      return loan_history_data

   def get_all(self, ten_id):
      loan_history_data = self.db.query(LoanHistory).filter(LoanHistory.ten_id == ten_id)
      return loan_history_data.all() if loan_history_data else None

   def get_by_id(self, loan_history_id: int):
      loan_history_data = self.db.query(LoanHistory).get(loan_history_id)
      return loan_history_data


class _CrudLoanSchedule():
   db: sessionmaker

   def __init__(self, db: sessionmaker):
      self.db = db

   def create(self, data: LoanSchedule):
      self.db.add(data)
      return data

   def edit(self, data):
      loan_schedule_data: LoanSchedule = self.db.query(LoanSchedule).get(data["id"])
      if loan_schedule_data:
         loan_schedule_data.fill(data)
      return loan_schedule_data

   def get_all(self, ten_id):
      loan_schedule_data = self.db.query(LoanSchedule).filter(LoanSchedule.ten_id == ten_id)
      return loan_schedule_data.all() if loan_schedule_data else None

   def get_by_id(self, loan_schedule_id: int):
      loan_schedule_data = self.db.query(LoanSchedule).get(loan_schedule_id)
      return loan_schedule_data


class _CrudLoanTransactions():
   db: sessionmaker

   def __init__(self, db: sessionmaker):
      self.db = db

   def create(self, data: LoanTransactions):
      self.db.add(data)
      return data

   def edit(self, data):
      loan_transactions_data: LoanTransactions = self.db.query(LoanTransactions).get(data["id"])
      if loan_transactions_data:
         loan_transactions_data.fill(data)
      return loan_transactions_data

   def get_all(self, ten_id):
      loan_transactions_data = self.db.query(LoanTransactions).filter(LoanTransactions.ten_id == ten_id)
      return loan_transactions_data.all() if loan_transactions_data else None

   def get_by_id(self, loan_transactions_id: int):
      loan_transactions_data = self.db.query(LoanTransactions).get(loan_transactions_id)
      return loan_transactions_data

