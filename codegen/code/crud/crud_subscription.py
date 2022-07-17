
from typing import List, Any, Optional, Type
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.subscription import SubscriptionPortfolio, SubscriptionProduct, SubscriptionTagRelation, SubscriptionTransaction
from app.schemas.subscription import SubscriptionPortfolioCreate, SubscriptionPortfolioUpdate
from app.schemas.subscription import SubscriptionProductCreate, SubscriptionProductUpdate
from app.schemas.subscription import SubscriptionTagRelationCreate, SubscriptionTagRelationUpdate
from app.schemas.subscription import SubscriptionTransactionCreate, SubscriptionTransactionUpdate

class CRUDSubscriptionPortfolio(CRUDBase[SubscriptionPortfolio, SubscriptionPortfolioCreate,SubscriptionPortfolioUpdate]):
   def create(self, db: Session, *, obj_in: SubscriptionPortfolioCreate, creator: str) -> SubscriptionPortfolio:
      obj_in_data = jsonable_encoder(obj_in)
      db_obj = self.model(**obj_in_data)
      db_obj.creator = creator
      db.add(db_obj)
      db.commit()
      db.refresh(db_obj)
      return db_obj

   def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[SubscriptionPortfolio]:
      return db.query(self.model).offset(skip).limit(limit).all()

   def get_all_active(self, db: Session) -> List[SubscriptionPortfolio]:
      return db.query(self.model).filter(self.model.date_ended == None).all()

   def get(self, db: Session, id: Any) -> Optional[SubscriptionPortfolio]:
      return db.query(self.model).filter(self.model.id == id).first()


class CRUDSubscriptionProduct(CRUDBase[SubscriptionProduct, SubscriptionProductCreate,SubscriptionProductUpdate]):
   def create(self, db: Session, *, obj_in: SubscriptionProductCreate, creator: str) -> SubscriptionProduct:
      obj_in_data = jsonable_encoder(obj_in)
      db_obj = self.model(**obj_in_data)
      db_obj.creator = creator
      db.add(db_obj)
      db.commit()
      db.refresh(db_obj)
      return db_obj

   def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[SubscriptionProduct]:
      return db.query(self.model).offset(skip).limit(limit).all()

   def get_all_active(self, db: Session) -> List[SubscriptionProduct]:
      return db.query(self.model).filter(self.model.date_ended == None).all()

   def get(self, db: Session, id: Any) -> Optional[SubscriptionProduct]:
      return db.query(self.model).filter(self.model.id == id).first()


class CRUDSubscriptionTagRelation(CRUDBase[SubscriptionTagRelation, SubscriptionTagRelationCreate,SubscriptionTagRelationUpdate]):
   def create(self, db: Session, *, obj_in: SubscriptionTagRelationCreate, creator: str) -> SubscriptionTagRelation:
      obj_in_data = jsonable_encoder(obj_in)
      db_obj = self.model(**obj_in_data)
      db_obj.creator = creator
      db.add(db_obj)
      db.commit()
      db.refresh(db_obj)
      return db_obj

   def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[SubscriptionTagRelation]:
      return db.query(self.model).offset(skip).limit(limit).all()

   def get_all_active(self, db: Session) -> List[SubscriptionTagRelation]:
      return db.query(self.model).filter(self.model.date_ended == None).all()

   def get(self, db: Session, id: Any) -> Optional[SubscriptionTagRelation]:
      return db.query(self.model).filter(self.model.id == id).first()


class CRUDSubscriptionTransaction(CRUDBase[SubscriptionTransaction, SubscriptionTransactionCreate,SubscriptionTransactionUpdate]):
   def create(self, db: Session, *, obj_in: SubscriptionTransactionCreate, creator: str) -> SubscriptionTransaction:
      obj_in_data = jsonable_encoder(obj_in)
      db_obj = self.model(**obj_in_data)
      db_obj.creator = creator
      db.add(db_obj)
      db.commit()
      db.refresh(db_obj)
      return db_obj

   def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[SubscriptionTransaction]:
      return db.query(self.model).offset(skip).limit(limit).all()

   def get_all_active(self, db: Session) -> List[SubscriptionTransaction]:
      return db.query(self.model).filter(self.model.date_ended == None).all()

   def get(self, db: Session, id: Any) -> Optional[SubscriptionTransaction]:
      return db.query(self.model).filter(self.model.id == id).first()


subscription_portfolio = CRUDSubscriptionPortfolio(SubscriptionPortfolio)
subscription_product = CRUDSubscriptionProduct(SubscriptionProduct)
subscription_tag_relation = CRUDSubscriptionTagRelation(SubscriptionTagRelation)
subscription_transaction = CRUDSubscriptionTransaction(SubscriptionTransaction)