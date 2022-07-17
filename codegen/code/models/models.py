import hashlib
from sqlalchemy import create_engine, ForeignKey, Table, Column, Integer, Float, String, Boolean, UniqueConstraint, Numeric, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from flask import Flask, jsonify
import datetime
from sqlalchemy_serializer import SerializerMixin
from urllib import parse
from base import Base


class User(Base, SerializerMixin):
    __tablename__ = "user"
    serialize_only = ("id", "ten_id", "username", "avatar", "fullname", "role", "status", "company", "profile", "password_status", "authtoken", "email", "phone", "created_on", "created_by")
    id = Column(Integer, primary_key=True, index=True)
    ten_id = Column(Integer, nullable=False)
    username = Column(String, nullable=True)
    avatar = Column(String)
    fullname = Column(String, nullable=False)
    role = Column(String)
    status = Column(String)
    company = Column(String)
    profile = Column(String)
    password_status = Column(String)
    authtoken = Column(String)
    email = Column(String)
    phone = Column(String)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    created_by = Column(Integer, nullable=False)

    def fill(self, _dict):
        self.__dict__.update(_dict)


class UserLogs(Base, SerializerMixin):
    __tablename__ = "user_logs"
    serialize_only = ("id", "ten_id", "user_id", "action_name", "action_time")
    id = Column(Integer, primary_key=True, index=True)
    ten_id = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="user_logs")
    action_name = Column(String)
    action_time = Column(DateTime, default=datetime.datetime.utcnow)

    def fill(self, _dict):
        self.__dict__.update(_dict)


class LoanProduct(Base, SerializerMixin):
    __tablename__ = "loan_product"
    serialize_only = ("id", "name", "description", "amount", "interest_rate", "interest_amount", "frequency", "guarantors", "guarantee_multi_loans", "guarantor_max_liability", "guarantee_above_savings", "savings_ratio", "savings_product", "allow_outstanding", "created_on", "created_by")
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    amount = Column(Float)
    interest_rate = Column(Float)
    interest_amount = Column(Float)
    frequency = Column(String)
    guarantors = Column(Integer)
    guarantee_multi_loans = Column(Boolean)
    guarantor_max_liability = Column(Float)
    guarantee_above_savings = Column(Boolean)
    savings_ratio = Column(Float)
    savings_product = Column(String)
    allow_outstanding = Column(Boolean)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    created_by = Column(Integer, ForeignKey("user.id"))
    user = relationship("User")

    def fill(self, _dict):
        self.__dict__.update(_dict)


class LoanApplication(Base, SerializerMixin):
    __tablename__ = "loan_application"
    serialize_only = ("id", "loan_product_id", "loan_acount_id", "loan_amount", "interest_rate", "interest_amount", "frequency", "installments", "purpose", "created_on", "created_by")
    id = Column(Integer, primary_key=True, index=True)
    loan_product_id = Column(Integer, ForeignKey("loan_product.id"), nullable=False)
    loan_product = relationship("LoanProduct")
    loan_acount_id = Column(Integer, ForeignKey("customer_account.id"), nullable=False)
    customer_account = relationship("CustomerAccount")
    loan_amount = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)
    interest_amount = Column(Float, nullable=False)
    frequency = Column(String, nullable=False)
    installments = Column(Integer, nullable=False)
    purpose = Column(String)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    created_by = Column(Integer, ForeignKey("user.id"))
    user = relationship("User")

    def fill(self, _dict):
        self.__dict__.update(_dict)


class Guarantee(Base, SerializerMixin):
    __tablename__ = "guarantee"
    serialize_only = ("id", "loan_id", "loan_account_id", "guarantor_id", "guarantee_amount", "approved", "approved_by", "approved_on", "created_on", "created_by")
    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(Integer, ForeignKey("loan_application.id"), nullable=False)
    loan_application = relationship("LoanApplication")
    loan_account_id = Column(String)
    guarantor_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    customers = relationship("Customers")
    guarantee_amount = Column(Float)
    approved = Column(Boolean)
    approved_by = Column(Integer, ForeignKey("user.id"))
    user = relationship("User")
    approved_on = Column(DateTime)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    created_by = Column(Integer, ForeignKey("user.id"))
    user = relationship("User")

    def fill(self, _dict):
        self.__dict__.update(_dict)


class LoanHistory(Base, SerializerMixin):
    __tablename__ = "loan_history"
    serialize_only = ("id", "loan_id", "action", "date", "naration", "status", "created_on", "created_by")
    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(Integer, ForeignKey("loan_application.id"), nullable=False)
    loan_application = relationship("LoanApplication")
    action = Column(String)
    date = Column(DateTime)
    naration = Column(String)
    status = Column(String)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    created_by = Column(Integer, ForeignKey("user.id"))
    user = relationship("User")

    def fill(self, _dict):
        self.__dict__.update(_dict)


class LoanSchedule(Base, SerializerMixin):
    __tablename__ = "loan_schedule"
    serialize_only = ("id", "loan_id", "loan_account_id", "due_date", "interest_due", "principal_due", "fees_due", "interest_paid", "principal_paid", "fees_paid", "interest_balance", "principal_balance", "fees_balance", "created_on", "created_by")
    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(Integer, ForeignKey("loan_application.id"), nullable=False)
    loan_application = relationship("LoanApplication")
    loan_account_id = Column(String)
    due_date = Column(DateTime)
    interest_due = Column(Float)
    principal_due = Column(Float)
    fees_due = Column(Float)
    interest_paid = Column(Float)
    principal_paid = Column(Float)
    fees_paid = Column(Float)
    interest_balance = Column(Float)
    principal_balance = Column(Float)
    fees_balance = Column(Float)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    created_by = Column(Integer, ForeignKey("user.id"))
    user = relationship("User")

    def fill(self, _dict):
        self.__dict__.update(_dict)


class LoanTransactions(Base, SerializerMixin):
    __tablename__ = "loan_transactions"
    serialize_only = ("id", "loan_id", "loan_account_id", "transaction_type", "narration", "amount", "principal", "interest", "fees", "principal_paid", "interest_paid", "fees_paid", "date", "created_on", "created_by")
    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(Integer, ForeignKey("loan_application.id"), nullable=False)
    loan_application = relationship("LoanApplication")
    loan_account_id = Column(String)
    transaction_type = Column(String)
    narration = Column(String)
    amount = Column(Float)
    principal = Column(Float)
    interest = Column(Float)
    fees = Column(Float)
    principal_paid = Column(Float)
    interest_paid = Column(Float)
    fees_paid = Column(Float)
    date = Column(DateTime)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    created_by = Column(Integer, ForeignKey("user.id"))
    user = relationship("User")

    def fill(self, _dict):
        self.__dict__.update(_dict)
