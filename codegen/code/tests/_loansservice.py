
from .utils import process_exception
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from crud import CrudLoanProductCrudLoanApplicationCrudGuaranteeCrudLoanHistoryCrudLoanScheduleCrudLoanTransactions
from modelsLoanProductLoanApplicationGuaranteeLoanHistoryLoanScheduleLoanTransactions

class LoansService:
   def list_loans(self, db: sessionmaker, ten_id: int):
      result = {"error": "", "data": []}
      try:
         pass
      except Exception as xxx:
         error = process_exception(xxx)
         result["error"] = error
         db.rollback()
      return result

   def lookup_loans(self, db: sessionmaker, data):
      result = {"error": "", "data": []}
      try:
         pass
      except Exception as xxx:
         error = process_exception(xxx)
         result["error"] = error
         db.rollback()
      return result

   def add_loans(self, db: sessionmaker, data):
      result = {"error": "", "data": []}
      try:
         pass
      except Exception as xxx:
         error = process_exception(xxx)
         result["error"] = error
         db.rollback()
      return result