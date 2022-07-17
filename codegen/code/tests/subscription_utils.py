
from app.models.utils import TransactionState
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.tests import utils

def create_random_subscription_portfolio(db: Session):
   customer = utils.get_random_customer()
   customer_id = customer.id
   isactive = False
   creator = utils.random_lower_string()
   subscription_portfolio_in = schemas.SubscriptionPortfolioCreate(customer_id = customer_id, isactive = isactive)
   subscription_portfolio = crud.subscription_portfolio.create(db=db, obj_in=subscription_portfolio_in, creator=creator)
   return subscription_portfolio

def create_random_subscription_product(db: Session):
   customer = utils.get_random_customer()
   customer_id = customer.id
   remote_order_item = utils.random_with_N_digits(3)
   subscription_portfolio = utils.get_random_subscription_portfolio()
   subscription_portfolio_id = subscription_portfolio.id
   country = utils.get_random_country()
   country_id = country.id
   currency = utils.get_random_currency()
   currency_id = currency.id
   paygo_plan = utils.get_random_paygo_plan()
   paygo_plan_id = paygo_plan.id
   creator = utils.random_lower_string()
   subscription_product_in = schemas.SubscriptionProductCreate(customer_id = customer_id, remote_order_item = remote_order_item, subscription_portfolio_id = subscription_portfolio_id, country_id = country_id, currency_id = currency_id, paygo_plan_id = paygo_plan_id)
   subscription_product = crud.subscription_product.create(db=db, obj_in=subscription_product_in, creator=creator)
   return subscription_product

def create_random_subscription_tag_relation(db: Session):
   subscription_product = utils.get_random_subscription_product()
   subscription_product_id = subscription_product.id
   tag = utils.get_random_tag()
   tag_id = tag.id
   creator = utils.random_lower_string()
   subscription_tag_relation_in = schemas.SubscriptionTagRelationCreate(subscription_product_id = subscription_product_id, tag_id = tag_id)
   subscription_tag_relation = crud.subscription_tag_relation.create(db=db, obj_in=subscription_tag_relation_in, creator=creator)
   return subscription_tag_relation

def create_random_subscription_transaction(db: Session):
   transaction_type = utils.get_random_transaction_type()
   transaction_type_id = transaction_type.id
   amount = utils.random_with_N_digits(3)
   subscription_product = utils.get_random_subscription_product()
   subscription_product_id = subscription_product.id
   subscription_transaction = utils.get_random_subscription_transaction()
   reversed_transaction_id = subscription_transaction.id
   token_rate = utils.random_with_N_digits(3)
   unredeemed_token_amount = utils.random_with_N_digits(3)
   number_of_tokens_units = utils.random_with_N_digits(3)
   token_blocking_fees = utils.random_with_N_digits(3)
   total_fees_paid = utils.random_with_N_digits(3)
   total_amount_received = utils.random_with_N_digits(3)
   total_discount_issued = utils.random_with_N_digits(3)
   state = TransactionState.ACTIVE.value
   creator = utils.random_lower_string()
   subscription_transaction_in = schemas.SubscriptionTransactionCreate(transaction_type_id = transaction_type_id, amount = amount, subscription_product_id = subscription_product_id, reversed_transaction_id = reversed_transaction_id, token_rate = token_rate, unredeemed_token_amount = unredeemed_token_amount, number_of_tokens_units = number_of_tokens_units, token_blocking_fees = token_blocking_fees, total_fees_paid = total_fees_paid, total_amount_received = total_amount_received, total_discount_issued = total_discount_issued, state = state)
   subscription_transaction = crud.subscription_transaction.create(db=db, obj_in=subscription_transaction_in, creator=creator)
   return subscription_transaction

"""
# models.__init__.py
from .subscription import SubscriptionPortfolio, SubscriptionProduct, SubscriptionTagRelation, SubscriptionTransaction

# crud.__init__.py
from .subscription import subscription_portfolio, subscription_product, subscription_tag_relation, subscription_transaction

# schema.__init__.py
from .subscription import SubscriptionPortfolioCreate, SubscriptionPortfolioInDB, SubscriptionPortfolioUpdate
from .subscription import SubscriptionProductCreate, SubscriptionProductInDB, SubscriptionProductUpdate
from .subscription import SubscriptionTagRelationCreate, SubscriptionTagRelationInDB, SubscriptionTagRelationUpdate
from .subscription import SubscriptionTransactionCreate, SubscriptionTransactionInDB, SubscriptionTransactionUpdate

"""