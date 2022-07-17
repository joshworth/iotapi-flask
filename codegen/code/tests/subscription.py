
from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from app.tests import utils
from app.models.utils import TransactionState

def test_create_subscription_portfolio(db: Session) -> None:
   customer = utils.get_random_customer()
   customer_id = customer.id
   isactive = False
   creator = utils.random_lower_string()
   subscription_portfolio_in = schemas.SubscriptionPortfolioCreate(customer_id = customer_id, isactive = isactive)
   subscription_portfolio = crud.subscription_portfolio.create(db=db, obj_in=subscription_portfolio_in, creator=creator)
   assert subscription_portfolio
   assert subscription_portfolio.customer_id == customer_id
   assert subscription_portfolio.isactive == isactive

def test_get_subscription_portfolio(db: Session) -> None:
   customer = utils.get_random_customer()
   customer_id = customer.id
   isactive = False
   creator = utils.random_lower_string()
   subscription_portfolio_in = schemas.SubscriptionPortfolioCreate(customer_id = customer_id, isactive = isactive)
   subscription_portfolio = crud.subscription_portfolio.create(db=db, obj_in=subscription_portfolio_in, creator=creator)
   subscription_portfolio_indb = crud.subscription_portfolio.get(db=db, id=subscription_portfolio.id)
   assert subscription_portfolio_indb
   assert subscription_portfolio.customer_id == customer_id
   assert subscription_portfolio.isactive == isactive

def test_get_multi_subscription_portfolio(db: Session) -> None:
   for _ in range(3):
      customer = utils.get_random_customer()
      customer_id = customer.id
      isactive = False
      creator = utils.random_lower_string()
      subscription_portfolio_in = schemas.SubscriptionPortfolioCreate(customer_id = customer_id, isactive = isactive)
      subscription_portfolio = crud.subscription_portfolio.create(db=db, obj_in=subscription_portfolio_in, creator=creator)
   subscription_portfolio_list = crud.subscription_portfolio.get_multi(db=db)
   assert subscription_portfolio_list
   assert len(subscription_portfolio_list) >= 3

def test_create_subscription_product(db: Session) -> None:
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
   assert subscription_product
   assert subscription_product.customer_id == customer_id
   assert subscription_product.remote_order_item == remote_order_item
   assert subscription_product.subscription_portfolio_id == subscription_portfolio_id
   assert subscription_product.country_id == country_id
   assert subscription_product.currency_id == currency_id
   assert subscription_product.paygo_plan_id == paygo_plan_id

def test_get_subscription_product(db: Session) -> None:
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
   subscription_product_indb = crud.subscription_product.get(db=db, id=subscription_product.id)
   assert subscription_product_indb
   assert subscription_product.customer_id == customer_id
   assert subscription_product.remote_order_item == remote_order_item
   assert subscription_product.subscription_portfolio_id == subscription_portfolio_id
   assert subscription_product.country_id == country_id
   assert subscription_product.currency_id == currency_id
   assert subscription_product.paygo_plan_id == paygo_plan_id

def test_get_multi_subscription_product(db: Session) -> None:
   for _ in range(3):
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
   subscription_product_list = crud.subscription_product.get_multi(db=db)
   assert subscription_product_list
   assert len(subscription_product_list) >= 3

def test_create_subscription_tag_relation(db: Session) -> None:
   subscription_product = utils.get_random_subscription_product()
   subscription_product_id = subscription_product.id
   tag = utils.get_random_tag()
   tag_id = tag.id
   creator = utils.random_lower_string()
   subscription_tag_relation_in = schemas.SubscriptionTagRelationCreate(subscription_product_id = subscription_product_id, tag_id = tag_id)
   subscription_tag_relation = crud.subscription_tag_relation.create(db=db, obj_in=subscription_tag_relation_in, creator=creator)
   assert subscription_tag_relation
   assert subscription_tag_relation.subscription_product_id == subscription_product_id
   assert subscription_tag_relation.tag_id == tag_id

def test_get_subscription_tag_relation(db: Session) -> None:
   subscription_product = utils.get_random_subscription_product()
   subscription_product_id = subscription_product.id
   tag = utils.get_random_tag()
   tag_id = tag.id
   creator = utils.random_lower_string()
   subscription_tag_relation_in = schemas.SubscriptionTagRelationCreate(subscription_product_id = subscription_product_id, tag_id = tag_id)
   subscription_tag_relation = crud.subscription_tag_relation.create(db=db, obj_in=subscription_tag_relation_in, creator=creator)
   subscription_tag_relation_indb = crud.subscription_tag_relation.get(db=db, id=subscription_tag_relation.id)
   assert subscription_tag_relation_indb
   assert subscription_tag_relation.subscription_product_id == subscription_product_id
   assert subscription_tag_relation.tag_id == tag_id

def test_get_multi_subscription_tag_relation(db: Session) -> None:
   for _ in range(3):
      subscription_product = utils.get_random_subscription_product()
      subscription_product_id = subscription_product.id
      tag = utils.get_random_tag()
      tag_id = tag.id
      creator = utils.random_lower_string()
      subscription_tag_relation_in = schemas.SubscriptionTagRelationCreate(subscription_product_id = subscription_product_id, tag_id = tag_id)
      subscription_tag_relation = crud.subscription_tag_relation.create(db=db, obj_in=subscription_tag_relation_in, creator=creator)
   subscription_tag_relation_list = crud.subscription_tag_relation.get_multi(db=db)
   assert subscription_tag_relation_list
   assert len(subscription_tag_relation_list) >= 3

def test_create_subscription_transaction(db: Session) -> None:
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
   assert subscription_transaction
   assert subscription_transaction.transaction_type_id == transaction_type_id
   assert subscription_transaction.amount == amount
   assert subscription_transaction.subscription_product_id == subscription_product_id
   assert subscription_transaction.reversed_transaction_id == reversed_transaction_id
   assert subscription_transaction.token_rate == token_rate
   assert subscription_transaction.unredeemed_token_amount == unredeemed_token_amount
   assert subscription_transaction.number_of_tokens_units == number_of_tokens_units
   assert subscription_transaction.token_blocking_fees == token_blocking_fees
   assert subscription_transaction.total_fees_paid == total_fees_paid
   assert subscription_transaction.total_amount_received == total_amount_received
   assert subscription_transaction.total_discount_issued == total_discount_issued
   assert subscription_transaction.state == state

def test_get_subscription_transaction(db: Session) -> None:
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
   subscription_transaction_indb = crud.subscription_transaction.get(db=db, id=subscription_transaction.id)
   assert subscription_transaction_indb
   assert subscription_transaction.transaction_type_id == transaction_type_id
   assert subscription_transaction.amount == amount
   assert subscription_transaction.subscription_product_id == subscription_product_id
   assert subscription_transaction.reversed_transaction_id == reversed_transaction_id
   assert subscription_transaction.token_rate == token_rate
   assert subscription_transaction.unredeemed_token_amount == unredeemed_token_amount
   assert subscription_transaction.number_of_tokens_units == number_of_tokens_units
   assert subscription_transaction.token_blocking_fees == token_blocking_fees
   assert subscription_transaction.total_fees_paid == total_fees_paid
   assert subscription_transaction.total_amount_received == total_amount_received
   assert subscription_transaction.total_discount_issued == total_discount_issued
   assert subscription_transaction.state == state

def test_get_multi_subscription_transaction(db: Session) -> None:
   for _ in range(3):
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
   subscription_transaction_list = crud.subscription_transaction.get_multi(db=db)
   assert subscription_transaction_list
   assert len(subscription_transaction_list) >= 3