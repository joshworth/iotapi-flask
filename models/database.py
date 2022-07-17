import hashlib
from sqlalchemy import create_engine, ForeignKey, Table, Column, Integer, Float, String, Boolean, UniqueConstraint, Numeric, DateTime, UniqueConstraint
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from flask import Flask, jsonify
import datetime
from sqlalchemy_serializer import SerializerMixin
from urllib import parse
import yaml

from base import Base


class Tennants(Base, SerializerMixin):
    __tablename__ = "tennants"
    serialize_only = ("id", "code", "fullname", "email", "detail", "created_on")
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    fullname = Column(String, unique=True, nullable=False)
    email = Column(String)
    phone = Column(String)
    detail = Column(String)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)

    def fill(self, data):
        if "code" in data:
            self.code = data["code"]
        if "fullname" in data:
            self.fullname = data["fullname"]
        if "email" in data:
            self.email = data["email"]
        if "phone" in data:
            self.phone = data["phone"]
        if "detail" in data:
            self.detail = data["detail"]


class Settings(Base, SerializerMixin):
    __tablename__ = "settings"
    serialize_only = ("id", "phrase", "detail", "runlevel", "created_on")
    id = Column(Integer, primary_key=True)
    ten_id = Column(Integer, nullable=False)
    phrase = Column(String, unique=True, nullable=False)
    detail = Column(String)
    runlevel = Column(Integer, default=0)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)

    def fill(self, data):
        if "phrase" in data:
            self.phrase = data["phrase"]
        if "detail" in data:
            self.detail = data["detail"]
        if "runlevel" in data:
            self.runlevel = data["runlevel"]


class User(Base, SerializerMixin):
    __tablename__ = "user"
    serialize_only = (
        "id",
        "ten_id",
        "username",
        "fullname",
        "role",
        "status",
        "company",
        "profile",
        "password",
        "password_status",
        "authtoken",
        "email",
        "phone",
        "created_on",
        "created_by",
    )
    # serialize_rules = ('-user_logs.user.user_logs',)

    id = Column(Integer, primary_key=True)
    ten_id = Column(Integer, nullable=False)
    username = Column(String, unique=True, nullable=False)
    avatar = Column(String)
    fullname = Column(String)
    role = Column(String)
    status = Column(String)
    company = Column(String)
    profile = Column(String)
    password = Column(String)
    password_status = Column(String)
    authtoken = Column(String)
    email = Column(String)
    phone = Column(String)
    # personal_info = Column(JSON)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    created_by = Column(Integer, nullable=False)
    user_logs = relationship("UserLogs", back_populates="user")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def fill(self, data):
        if "username" in data:
            self.username = data["username"]
        if "fullname" in data:
            self.fullname = data["fullname"]
        if "role" in data:
            self.role = data["role"]
        if "status" in data:
            self.status = data["status"]
        if "company" in data:
            self.company = data["company"]
        if "profile" in data:
            self.profile = data["profile"]
        if "password" in data:
            self.password = data["password"]
        if "password_status" in data:
            self.password_status = data["password_status"]
        if "authtoken" in data:
            self.authtoken = data["authtoken"]
        if "email" in data:
            self.email = data["email"]
        if "phone" in data:
            self.phone = data["phone"]
        if "created_by" in data:
            self.created_by = data["created_by"]


class UserLogs(Base, SerializerMixin):
    __tablename__ = "user_logs"
    serialize_only = ("id", "user_id", "action_name", "action_time")
    id = Column(Integer, primary_key=True)
    ten_id = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    action_name = Column(String)
    action_time = Column(DateTime, default=datetime.datetime.utcnow)
    user = relationship("User", back_populates="user_logs")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Customer(Base, SerializerMixin):
    __tablename__ = "customer"
    serialize_only = ("id", "customer_name", "trading_name", "account_prefix", "customer_type", "address", "location", "country", "primary_phone", "secondary_phone", "email", "tax_no", "avatar", "created_on", "ten_id")
    id = Column(Integer, primary_key=True)
    ten_id = Column(Integer, nullable=False)
    customer_name = Column(String, unique=True, nullable=False)
    trading_name = Column(String, unique=True, nullable=False)
    account_prefix = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", backref="customer")
    customer_type = Column(String, nullable=False)
    address = Column(String, nullable=False)
    location = Column(String)
    country = Column(String)
    primary_phone = Column(String, unique=True, nullable=False)
    secondary_phone = Column(String)
    email = Column(String)
    tax_no = Column(String)
    avatar = Column(String)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    customer_accounts = relationship("CustomerAccount", back_populates="customer")

    def fill(self, data):
        if "customer_name" in data:
            self.customer_name = data["customer_name"]
        if "trading_name" in data:
            self.trading_name = data["trading_name"]
        if "account_prefix" in data:
            self.account_prefix = data["account_prefix"]
        if "customer_type" in data:
            self.customer_type = data["customer_type"]
        if "address" in data:
            self.address = data["address"]
        if "address" in data:
            self.address = data["address"]
        if "location" in data:
            self.location = data["location"]
        if "country" in data:
            self.country = data["country"]
        if "primary_phone" in data:
            self.primary_phone = data["primary_phone"]
        if "secondary_phone" in data:
            self.secondary_phone = data["secondary_phone"]
        if "email" in data:
            self.email = data["email"]
        if "tax_no" in data:
            self.tax_no = data["tax_no"]
        if "ten_id" in data:
            self.ten_id = data["ten_id"]


class CustomerAccount(Base, SerializerMixin):
    __tablename__ = "customer_account"
    serialize_only = ("id", "customer_id", "account_no", "account_type", "facility_id", "account_priority", "device_id", "balance", "last_transaction_amount", "last_transaction_date", "last_transaction_type", "next_due_date", "status", "created_on", "started_on", "ten_id")
    id = Column(Integer, primary_key=True)
    ten_id = Column(Integer, nullable=False)
    customer_id = Column(Integer, ForeignKey("customer.id"))
    account_no = Column(String, unique=True, nullable=False)
    account_type = Column(String, unique=True, nullable=False)
    facility_id = Column(Integer, nullable=False)
    account_priority = Column(Integer, nullable=False)
    started_on = Column(DateTime, default=datetime.datetime.utcnow)
    device_id = Column(Integer, ForeignKey("device.id"))
    balance = Column(Float)
    last_transaction_amount = Column(Float)
    last_transaction_date = Column(DateTime)
    last_transaction_type = Column(String)
    next_due_date = Column(DateTime)
    status = Column(String)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    customer = relationship("Customer", back_populates="customer_accounts")
    device = relationship("Device", back_populates="customer_account")
    customer_transactions = relationship("CustomerTransactions", back_populates="customer_account")

    def fill(self, data):
        if "customer_id" in data:
            self.customer_id = data["customer_id"]
        if "account_no" in data:
            self.account_no = data["account_no"]
        if "account_type" in data:
            self.account_type = data["account_type"]
        if "facility_id" in data:
            self.facility_id = data["facility_id"]
        if "account_priority" in data:
            self.account_priority = data["account_priority"]
        if "device_id" in data:
            self.device_id = data["device_id"]
        if "balance" in data:
            self.balance = data["balance"]
        if "last_transaction_amount" in data:
            self.last_transaction_amount = data["last_transaction_amount"]
        if "last_transaction_date" in data:
            self.last_transaction_date = data["last_transaction_date"]
        if "last_transaction_type" in data:
            self.last_transaction_type = data["last_transaction_type"]
        if "next_due_date" in data:
            self.next_due_date = data["next_due_date"]
        if "status" in data:
            self.status = data["status"]
        if "ten_id" in data:
            self.ten_id = data["ten_id"]
        if "started_on" in data:
            self.started_on = data["started_on"]


class CustomerTransactions(Base, SerializerMixin):
    __tablename__ = "customer_transactions"
    serialize_only = ("id", "customer_account_id", "transaction_type", "transaction_code", "description", "amount", "date", "drcr", "balance", "created_on", "user_id", "ten_id")
    id = Column(Integer, primary_key=True)
    ten_id = Column(Integer, nullable=False)
    customer_account_id = Column(Integer, ForeignKey("customer_account.id"))
    transaction_type = Column(String)
    transaction_code = Column(String)
    description = Column(String)
    amount = Column(Float)
    date = Column(DateTime)
    drcr = Column(String)
    balance = Column(Float)
    user_id = Column(Integer, ForeignKey("user.id"))
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    customer_account = relationship("CustomerAccount", back_populates="customer_transactions")

    def fill(self, data):
        if "customer_account_id" in data:
            self.customer_account_id = data["customer_account_id"]
        if "transaction_type" in data:
            self.transaction_type = data["transaction_type"]
        if "description" in data:
            self.description = data["description"]
        if "amount" in data:
            self.amount = data["amount"]
        if "drcr" in data:
            self.drcr = data["drcr"]
        if "balance" in data:
            self.balance = data["balance"]
        if "date" in data:
            self.date = data["date"]
        if "ten_id" in data:
            self.ten_id = data["ten_id"]
        if "drcr" in data:
            self.drcr = data["drcr"]
        if "user_id" in data:
            self.user_id = data["user_id"]
        if "transaction_code" in data:
            self.transaction_code = data["transaction_code"]


class Device(Base, SerializerMixin):
    __tablename__ = "device"
    serialize_only = ("id", "serial_number", "device_type", "barcode", "parent_id", "avatar", "device_key", "status", "created_on", "ten_id")

    id = Column(Integer, primary_key=True)
    ten_id = Column(Integer, nullable=False)
    serial_number = Column(String, unique=True, nullable=False)
    device_type = Column(String, nullable=False)
    barcode = Column(String, unique=True, nullable=True)
    parent_id = Column(String)
    avatar = Column(String)
    device_key = Column(String)
    status = Column(String)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    device_logs = relationship("DeviceLogs", back_populates="device")
    customer_account = relationship("CustomerAccount", back_populates="device")

    def fill(self, data):
        if "serial_number" in data:
            self.serial_number = data["serial_number"]
        if "device_type" in data:
            self.device_type = data["device_type"]
        if "barcode" in data:
            self.barcode = data["barcode"]
        if "parent_id" in data:
            self.parent_id = data["parent_id"]
        if "device_key" in data:
            self.device_key = data["device_key"]
        if "status" in data:
            self.status = data["status"]
        if "ten_id" in data:
            self.ten_id = data["ten_id"]


class DeviceLogs(Base, SerializerMixin):
    __tablename__ = "device_logs"

    serialize_only = ("id", "device_id", "amount", "volume", "topup", "post_time")
    id = Column(Integer, primary_key=True)
    ten_id = Column(Integer, nullable=False)
    device_id = Column(Integer, ForeignKey("device.id"))
    amount = Column(Float)
    volume = Column(Float)
    topup = Column(Float)
    post_time = Column(DateTime, default=datetime.datetime.utcnow)
    device = relationship("Device", back_populates="device_logs")
    detail = Column(String)

    def fill(self, data):
        if "device_id" in data:
            self.device_id = data["device_id"]
        if "amount" in data:
            self.amount = data["amount"]
        if "volume" in data:
            self.volume = data["volume"]
        if "topup" in data:
            self.topup = data["topup"]
        if "detail" in data:
            self.detail = data["detail"]


class ImportLogs(Base, SerializerMixin):
    __tablename__ = "import_logs"

    serialize_only = ("id", "ten_id", "file_id", "size", "path", "detail", "created_on", "created_by")
    id = Column(Integer, primary_key=True)
    ten_id = Column(Integer, nullable=False)
    file_id = Column(String, nullable=False)
    size = Column(Integer)
    path = Column(String)
    detail = Column(String)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    created_by = Column(Integer, ForeignKey("user.id"))
    UniqueConstraint("ten_id", "file_id", name="unique_file_id")

    def fill(self, data):
        if "ten_id" in data:
            self.ten_id = data["ten_id"]
        if "file_id" in data:
            self.file_id = data["file_id"]
        if "size" in data:
            self.size = data["size"]
        if "path" in data:
            self.path = data["path"]
        if "detail" in data:
            self.detail = data["detail"]
        if "created_on" in data:
            self.created_on = data["created_on"]
        if "created_by" in data:
            self.created_by = data["created_by"]


class GsmPost(Base, SerializerMixin):
    __tablename__ = "gsm_post"
    id = Column(Integer, primary_key=True)
    ten_id = Column(Integer, nullable=False)
    device_id = Column(String)
    amount = Column(Numeric)
    volume = Column(Numeric)
    topup = Column(Numeric)
    post_time = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, device_id, amount, volume, topup):
        self.device_id = device_id
        self.amount = amount
        self.volume = volume
        self.topup = topup

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def serialize(self):
        ser_det = {}
        for c in self.__table__.columns:
            val = getattr(self, c.name)
            # handle decimal conversion for serialization
            if c.name in ["amount", "volume", "topup"]:
                val = float(val)
            ser_det[c.name] = val

        return ser_det


# Base.metadata.create_all(engine)
