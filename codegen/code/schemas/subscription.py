
from datetime import date, datetime, time, timedelta
from typing import Optional, List
from pydantic import BaseModel

class SubscriptionPortfolioCreate(BaseModel):
   customer_id: int
   isactive: Optional[bool]

class SubscriptionPortfolioUpdate(BaseModel):
   customer_id: int
   isactive: Optional[bool]

class SubscriptionPortfolioInDB(BaseModel):
   id: int
   customer_id: int
   isactive: Optional[bool]

class SubscriptionProductCreate(BaseModel):
   customer_id: int
   remote_order_item: int
   subscription_portfolio_id: int
   country_id: int
   currency_id: int
   paygo_plan_id: int

class SubscriptionProductUpdate(BaseModel):
   id: Optional[int]
   customer_id: Optional[int]
   remote_order_item: Optional[int]
   subscription_portfolio_id: Optional[int]
   last_transaction_id: Optional[int]

class SubscriptionProductInDB(BaseModel):
   id: Optional[int]
   customer_id: Optional[int]
   remote_order_item: Optional[int]
   subscription_portfolio_id: Optional[int]
   country_id: Optional[int]
   currency_id: Optional[int]
   paygo_plan_id: int
   last_transaction_id: Optional[int]

class SubscriptionTagRelationCreate(BaseModel):
   subscription_product_id: int
   tag_id: int

class SubscriptionTagRelationUpdate(BaseModel):
   subscription_product_id: Optional[int]
   tag_id: Optional[int]

class SubscriptionTagRelationInDB(BaseModel):
   id: int
   subscription_product_id: Optional[int]
   tag_id: Optional[int]
   creator: Optional[str]

class SubscriptionTransactionCreate(BaseModel):
   transaction_type_id: int
   amount: int
   subscription_product_id: int
   reversed_transaction_id: Optional[int]
   token_rate: Optional[int]
   unredeemed_token_amount: Optional[int]
   number_of_tokens_units: Optional[int]
   token_blocking_fees: Optional[int]
   total_fees_paid: Optional[int]
   total_amount_received: Optional[int]
   total_discount_issued: Optional[int]
   state: Optional[TransactionState]

class SubscriptionTransactionUpdate(BaseModel):
   id: int
   transaction_type_id: Optional[int]
   amount: Optional[int]
   subscription_product_id: Optional[int]
   reversed_transaction_id: Optional[int]
   token_rate: Optional[int]
   unredeemed_token_amount: Optional[int]
   number_of_tokens_units: Optional[int]
   token_blocking_fees: Optional[int]
   total_fees_paid: Optional[int]
   total_amount_received: Optional[int]
   total_discount_issued: Optional[int]
   state: Optional[TransactionState]

class SubscriptionTransactionInDB(BaseModel):
   id: int
   transaction_type_id: Optional[int]
   amount: Optional[int]
   subscription_product_id: Optional[int]
   reversed_transaction_id: Optional[int]
   token_rate: Optional[int]
   unredeemed_token_amount: Optional[int]
   number_of_tokens_units: Optional[int]
   portion_fees: Optional[int]
   token_blocking_fees: Optional[int]
   total_fees_paid: Optional[int]
   total_amount_received: Optional[int]
   total_discount_issued: Optional[int]
   state: Optional[TransactionState]