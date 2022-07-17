
from sqlalchemy import Column, Integer, String, DateTime,  ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING
from .utils import TransactionState
import datetime
from app.db.base_class import Base

class SubscriptionPortfolio(Base):
   id = Column(Integer, primary_key=True, index=True)
   customer_id = Column(Integer, ForeignKey("customer.id"))
   customer = relationship("Customer")
   creator = Column(String, nullabe=True)
   date_added = Column(DateTime, default=datetime.datetime.utcnow)
   date_last_modified = Column(DateTime, nullabe=False)
   isactive = Column(Boolean, default=False)
   status = Column(String)

class SubscriptionProduct(Base):
   id = Column(Integer, primary_key=True, index=True)
   customer_id = Column(Integer, ForeignKey("customer.id"))
   customer = relationship("Customer")
   remote_order_item = Column(Integer, default=0)
   product_type = Column(Integer, default=0)
   subscription_portfolio_id = Column(Integer, ForeignKey("subscription_portfolio.id"))
   subscription_portfolio = relationship("SubscriptionPortfolio", back_populates="subscription_products")
   country_id = Column(Integer, ForeignKey("country.id"))
   country = relationship("Country")
   currency_id = Column(Integer, ForeignKey("currency.id"))
   currency = relationship("Currency")
   paygo_plan_id = Column(Integer, ForeignKey("paygo_plan.id"))
   paygo_plan = relationship("PaygoPlan")
   last_transaction_id = Column(Integer, ForeignKey("subscription_transaction.id"), nullabe=True)
   subscription_transaction = relationship("SubscriptionTransaction")
   date_added = Column(DateTime, default=datetime.datetime.utcnow)
   date_last_modified = Column(DateTime, nullabe=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
   creator = Column(String, nullabe=True)

class SubscriptionTagRelation(Base):
   id = Column(Integer, primary_key=True, index=True)
   subscription_product_id = Column(Integer, ForeignKey("subscription_product.id"))
   subscription_product = relationship("SubscriptionProduct")
   tag_id = Column(Integer, ForeignKey("tag.id"))
   tag = relationship("Tag")
   date_added = Column(DateTime, default=datetime.datetime.utcnow)
   date_last_modified = Column(DateTime, nullabe=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
   creator = Column(String, nullabe=True)

class SubscriptionTransaction(Base):
   id = Column(Integer, primary_key=True, index=True)
   transaction_type_id = Column(Integer, ForeignKey("transaction_type.id"))
   transaction_type = relationship("TransactionType")
   amount = Column(Integer)
   subscription_product_id = Column(Integer, ForeignKey("subscription_product.id"), nullabe=False)
   subscription_product = relationship("SubscriptionProduct")
   reversed_transaction_id = Column(Integer, ForeignKey("subscription_transaction.id"), nullabe=True)
   subscription_transaction = relationship("SubscriptionTransaction")
   token_rate = Column(Integer)
   unredeemed_token_amount = Column(Integer, default=0)
   number_of_tokens_units = Column(Integer, default=0)
   portion_fees = Column(Integer, default=0)
   token_blocking_fees = Column(Integer, default=0)
   total_fees_paid = Column(Integer, default=0)
   total_amount_received = Column(Integer, default=0)
   total_discount_issued = Column(Integer, default=0)
   state = Column(Enum(TransactionState), name="state_state")
   date_added = Column(DateTime, nullabe=False, default=datetime.datetime.utcnow)
   date_last_modified = Column(DateTime, nullabe=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
   creator = Column(String, nullabe=True)