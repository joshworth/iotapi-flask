from crud import CrudCustomer, CrudCustomerAccount, CrudCustomerTransactions, CrudDevice, CrudImportlogs
from models import Customer, CustomerAccount, CustomerTransactions, User, ImportLogs
from .utils import process_exception
from sqlalchemy.orm import sessionmaker
from datetime import datetime


DR_TRANSACTIONS = ["WITHDRAW", "PENALTY", "CHARGE", "BILL", "SAVINGS WITHDRAW"]
CR_TRANSACTIONS = ["DEPOSIT", "REFUND", "REWARD", "GIFT", "SAVINGS DEPOSIT"]

TRANSACTION_TYPE_LIST = [{"id": "SAVINGS DEPOSIT", "account": "SAVINGS", "action": "CR"}, {"id": "SAVINGS WITHDRAW", "account": "SAVINGS", "action": "DR"}, {"id": "INVESTMENT DEPOSIT", "account": "INVESTMENT", "action": "CR"}, {"id": "INVESTMENT WITHDRAW", "account": "INVESTMENT", "action": "DR"}, {"id": "LOAN DISBURSEMENT", "account": "LOANS", "action": "CR"}, {"id": "LOAN PAYMENT", "account": "LOANS", "action": "DR"}, {"id": "LOAN PENALTY", "account": "LOANS", "action": "CR"}, {"id": "WELFARE CHARGE", "account": "WELFARE", "action": "CR"}, {"id": "WELFARE PAYMENT", "account": "WELFARE", "action": "DR"}, {"id": "WELFARE PENALTY", "account": "WELFARE", "action": "CR"}, {"id": "MEMBERSHIP CHARGE", "account": "MEMBERSHIP", "action": "CR"}, {"id": "MEMBERSHIP PAYMENT", "account": "MEMBERSHIP", "action": "DR"}]


class CustomerService:
    def get_transaction_stamp(self):
        tstamp = time.time_ns()
        return str(tstamp)

    def list_customers(self, db: sessionmaker, ten_id: int):
        result = {"error": "", "data": []}
        try:
            cust_list = CrudCustomer(db).get_all(ten_id)
            for item in cust_list:
                pitem = item.to_dict()
                # add some other related inf summaries
                result["data"].append(pitem)
        except Exception as xxx:
            error = process_exception(xxx)
            result["error"] = error
            db.rollback()
        return result

    def list_customers_summary(self, db: sessionmaker, ten_id: int):
        result = {"error": "", "data": []}
        try:
            cust_list = CrudCustomer(db).get_all_summary(ten_id)

            for item in cust_list:
                # print("item.customer_accounts ==========",item.customer_accounts)
                acclist = []
                for acc in item.customer_accounts:
                    acclist.append({"id": acc.id, "account_no": acc.account_no, "account_type": acc.account_type})

                pitem = {"id": item.id, "customer_name": item.customer_name, "customer_type": item.customer_type, "account_prefix": item.account_prefix, "accounts": acclist}
                # add some other related inf summaries
                result["data"].append(pitem)
        except Exception as xxx:
            error = process_exception(xxx)
            result["error"] = error
            db.rollback()
        return result

    def lookup_customer(self, db: sessionmaker, data):
        result = {"error": "", "data": []}
        try:
            qlimit = 10
            cust_list = CrudCustomer(db).lookup_customer(data["ten_id"], data["tag"], data["account_no"], data["customer_name"], qlimit)
            for item in cust_list:
                pitem = {"id": item.id, "account_prefix": item.account_prefix, "customer_name": item.customer_name, "customer_type": item.customer_type, "primary_phone": item.primary_phone, "ten_id": item.ten_id}
                # add some other related inf summaries
                result["data"].append(pitem)
        except Exception as xxx:
            error = process_exception(xxx)
            result["error"] = error
            db.rollback()
        return result

    def add_customer(self, db: sessionmaker, data):
        result = {"error": "", "data": []}
        try:
            customer = Customer()
            print("============= cust x 0  ", data)

            customer_data = data
            # print("============= cust x 1  ", customer_data)
            if "account_prefix" not in customer_data or len(customer_data["account_prefix"]) == 0:
                customer_data["account_prefix"] = customer_data["primary_phone"]
            if "trading_name" not in customer_data or len(customer_data["trading_name"]) == 0:
                customer_data["trading_name"] = customer_data["customer_name"]
            customer.fill(customer_data)
            cust = CrudCustomer(db).create(customer)

            # print("============= cust x 1  ", cust.to_dict())
            # any accounts add them too
            acclist = []
            ser = 0  # add serial to product number for uniqueness
            for acc in customer_data["accounts"]:
                # do we have valid barcodes for types that need them?
                print("acc =============== ", acc)
                device_id = None
                if acc["device_barcode"] != "" or acc["account_type"] in ["DEVICE", "SUBSCRIPTION"]:
                    dev = CrudDevice(db).get_by_barcode(customer.ten_id, acc["device_barcode"])
                    if not dev:
                        result["error"] = f"ERROR: Device barcode {acc['device_barcode']} not found"
                        db.rollback()
                        return result

                    # is device already assigned
                    devacc = CrudCustomerAccount(db).get_by_device_id_active(dev.id)
                    if devacc:
                        result["error"] = f"ERROR: Device barcode {acc['device_barcode']} already assigned to a customer."
                        db.rollback()
                        return result

                    device_id = dev.id

                ser += 1
                # prepare relevant fields
                new_acc = {"account_no": f'{customer_data["account_prefix"]}{ser}', "account_priority": acc["account_priority"], "account_type": acc["account_type"], "device_id": device_id, "status": acc["status"], "ten_id": customer_data["ten_id"]}

                customer_acc = CustomerAccount()
                customer_acc.fill(new_acc)
                cacc = CrudCustomerAccount(db).create(customer_acc)
                acclist.append(cacc)
            db.commit()
            print("============= cust x ", cust.to_dict())
            acc["customer_id"] = cust
            # now update ids
            try:
                for acc in acclist:
                    dbacc = CrudCustomerAccount(db).get_by_id(acc.id)
                    dbacc.customer_id = cust.id
                db.commit()
                result["data"] = "Success"
            except Exception as exp:
                # error = process_exception(xxx)
                result["error"] = "Error while updating child customer accounts."
                db.rollback()
        except Exception as xxx:
            print("error===========", str(xxx))
            error = process_exception(xxx)
            result["error"] = error
            db.rollback()
        return result

    def add_customer_bulk(self, db: sessionmaker, data, logdata):
        result = {"error": "", "data": []}
        try:
            print("================== add_customer_bulk")
            saved_accounts = []
            for item in data:
                print("Adding ....... item... ", item)
                item["primary_phone"] = item["primary_phone"].replace("#", "") if item["primary_phone"] else ""
                item["secondary_phone"] = item["secondary_phone"].replace("#", "") if item["secondary_phone"] else ""
                item["account_prefix"] = item["primary_phone"]
                item["trading_name"] = item["customer_name"]
                # if accounts are defined create them
                acc_list = []
                acc_labels = ["account1", "account2", "account3", "account4"]
                pref = 0
                for lab in acc_labels:
                    pref += 1
                    if len(item[lab]) > 0:
                        acc_list.append({"ten_id": item["ten_id"], "account_no": f'{item["account_prefix"]}{pref}', "account_type": item[lab], "account_priority": pref, "status": "ACTIVE"})

                customer = Customer()
                customer.fill(item)
                cust = CrudCustomer(db).create(customer)
                for new_acc in acc_list:
                    customer_acc = CustomerAccount()
                    customer_acc.fill(new_acc)
                    cacc = CrudCustomerAccount(db).create(customer_acc)
                    saved_accounts.append([cust, cacc])
            db.commit()
            try:
                for arr in saved_accounts:
                    print("updating =============== ", arr[1].id, arr[1].account_no)
                    dbacc = CrudCustomerAccount(db).get_by_id(arr[1].id)
                    dbacc.customer_id = arr[0].id
                    print("done updating =============== ", arr[1].id, arr[1].account_no)

                # success log import
                print("log == import === ", logdata)
                imp = ImportLogs()
                imp.fill(logdata)
                CrudImportlogs(db).create(imp)

                db.commit()
                result["data"] = "Success"
            except Exception as exp:
                print(exp)
                # error = process_exception(xxx)
                result["error"] = "Error while updating child customer accounts."
                db.rollback()

        except Exception as xxx:
            print("error===========", str(xxx))
            error = process_exception(xxx)
            result["error"] = error
            db.rollback()
        return result

    def get_customer(self, db: sessionmaker, id):
        result = {"error": "", "data": ""}
        proc = 0
        try:
            customer: Customer = CrudCustomer(db).get_by_id(id)
            # format data
            if customer:
                rcust = customer.to_dict()
                # add accounts
                accounts = []
                txns = []
                proc = 1
                for acc in customer.customer_accounts:
                    barcode = acc.device.barcode if acc.device else ""
                    pacc = acc.to_dict()
                    pacc["device_barcode"] = barcode
                    accounts.append(pacc)
                    for txn in acc.customer_transactions:
                        cus_txn = txn.to_dict()
                        cus_txn["account_no"] = txn.customer_account.account_no
                        cus_txn["account_type"] = txn.customer_account.account_type
                        txns.append(cus_txn)
                proc = 2
                rcust["accounts"] = accounts
                rcust["transactions"] = txns

                rcust["user_id"] = ""
                rcust["user_name"] = ""
                rcust["has_login"] = False
                rcust["login_status"] = ""
                rcust["role"] = ""
                proc = 3
                if customer.user:
                    user: User = customer.user
                    proc = 3.1
                    rcust["user_id"] = user.id
                    rcust["user_name"] = user.username
                    rcust["has_login"] = True
                    rcust["login_status"] = user.status
                    rcust["role"] = user.role

                result["data"] = rcust

        except Exception as xxx:
            print("===== proc", proc)
            error = process_exception(xxx)
            result["error"] = error
            db.rollback()
        return result

    def get_account_action(self, transation_type):
        for tr in TRANSACTION_TYPE_LIST:
            if tr["id"] == transation_type:
                return tr["action"]

        return ""

    def add_customer_transaction(self, db: sessionmaker, data):
        result = {"error": "", "data": ""}
        try:
            # amount
            if type(data["amount"]) == str:
                data["amount"] = float(data["amount"])

            txcode = self.get_transaction_stamp()
            data["transaction_code"] = txcode
            # add current date
            now_time = datetime.now()
            data["date"] = now_time

            transaction = CustomerTransactions()
            transaction.fill(data)
            print("transaction amount typ ============ ", type(transaction.amount))

            acc: CustomerAccount = CrudCustomerAccount(db).get_by_id(transaction.customer_account_id)

            drcr = self.get_account_action(transaction.transaction_type)
            if len(drcr) == 0:
                result["error"] = f"ERROR: Transaction type {transaction.transaction_type} unknown."
                return result
            transaction.drcr = drcr

            print("acc ============ ", data)
            print(transaction.to_dict())
            # update account balance, if applicable

            print("acc ============ ", acc)
            balance = acc.balance if acc.balance else 0
            print("===types=== acc ============ cr", type(balance), type(transaction.amount))

            if drcr == "CR":
                acc.balance = balance + transaction.amount
            else:
                print("acc ============ dr")
                acc.balance = balance - transaction.amount

            print("acc ============ cr 2")
            acc.last_transaction_date = now_time
            acc.last_transaction_type = transaction.transaction_type
            acc.last_transaction_amount = transaction.amount

            print("acc ============ cr 3")
            transaction.drcr = drcr
            transaction.balance = acc.balance
            CrudCustomerTransactions(db).create(transaction)

            # determine if to update due date, for pmt
            # if payment for loan or subscription, determin by how much it extends due date

            db.commit()
            print("trans===success ==", transaction.to_dict())
            result["data"] = "Success"
        except Exception as xxx:
            error = process_exception(xxx)
            result["error"] = error
            db.rollback()
        return result

    def add_customer_transaction_bulk(self, db: sessionmaker, data, logdata):
        result = {"error": "", "data": "", "errors": []}
        import_errors = []
        try:
            found_acounts = []
            found_account_map = {}
            for item in data:
                # fix date
                date_obj = datetime.strptime(item["date"], "%d/%m/%Y")
                item["date"] = date_obj
                # lookup account_id
                if item["account_no"] not in found_acounts:
                    cdata = CrudCustomerAccount(db).get_by_account_no(item["ten_id"], item["account_no"])
                    if not cdata:
                        result["errors"].append(f"ERROR: Customer account {item['account_no']} not found.")
                    found_acounts.append(item["account_no"])
                    citem = {"account": cdata, "list": [item]}
                    found_account_map[item["account_no"]] = citem

                else:
                    found_account_map[item["account_no"]]["list"].append(item)

            # print("================= found", found_account_map)

            transaction_code = self.get_transaction_stamp()
            # now process each grou
            for acc in found_acounts:
                acc_id = found_account_map[acc]["account"].id
                for txn in found_account_map[acc]["list"]:
                    txn["customer_account_id"] = acc_id
                    txn["user_id"] = logdata["created_by"]
                    txn["transaction_code"] = transaction_code
                # sort
                new_accountlist = sorted(found_account_map[acc]["list"], key=lambda i: i["date"])

                print("sorted ===================== ", new_accountlist)

                accountdata: CustomerAccount = CrudCustomerAccount(db).get_by_id(acc_id)

                # get balance
                balance = found_account_map[acc]["account"].balance if found_account_map[acc]["account"].balance else 0
                last_txn = {}
                for txn in new_accountlist:
                    action_name = f"{accountdata.account_type} {txn['transaction_type']}"
                    drcr = self.get_account_action(action_name)
                    if drcr == "":
                        result["error"] = result["errors"].append(f"ERROR: Transaction type {action_name} unknown.")
                        return result

                    txn["drcr"] = drcr
                    # print("txn============ amount =====", txn["amount"])
                    amount_val = float(txn["amount"]) if type(txn["amount"]) == str else txn["amount"]
                    if drcr == "CR":
                        txn["balance"] = balance + amount_val
                    else:
                        # print("acc ============ dr")
                        txn["balance"] = balance - amount_val

                    # set account balance to new txn balance
                    balance = txn["balance"]
                    last_txn = txn

                    # print("prepared txn ======= ", txn)
                    print("amount==balance", txn["account_no"], drcr, amount_val, txn["balance"], balance)

                # now update db
                for txn in new_accountlist:
                    transaction = CustomerTransactions()
                    print("filling txxn ===========================", txn)
                    transaction.fill(txn)
                    print(" ======== transaction.user_id == ", transaction.user_id)
                    CrudCustomerTransactions(db).create(transaction)

                # update account balance
                accountdata.balance = last_txn["balance"]
                accountdata.last_transaction_amount = last_txn["amount"]
                accountdata.last_transaction_type = last_txn["transaction_type"]
                accountdata.last_transaction_date = last_txn["date"]

            # success log import
            imp = ImportLogs()
            imp.fill(logdata)
            CrudImportlogs(db).create(imp)
            if len(result["errors"]) == 0:
                db.commit()
                # print("trans===success ==", transaction.to_dict())
                result["data"] = "Success"
            else:
                result["error"] = "ERROR: There were importation error(s)."
        except Exception as xxx:
            error = process_exception(xxx)
            result["error"] = error
            db.rollback()
        return result

    def add_group_transaction(self, db: sessionmaker, data):
        result = {"error": "", "data": "", "errors": []}
        try:
            transaction_code = self.get_transaction_stamp()
            trans_data = data["transaction"]
            # fix date
            date_obj = datetime.strptime(trans_data["date"], "%Y-%m-%d")
            trans_data["date"] = date_obj
            trans_type = trans_data["transaction"]
            drcr = self.get_account_action(trans_type)
            if drcr == "":
                result["error"] = result["errors"].append(f"ERROR: Transaction type {trans_type} unknown.")
                return result
            for item in data["customer_list"]:
                # get balance
                acc_id = item["customer_account_id"]
                balance = CrudCustomerAccount(db).calculate_balance(data["ten_id"], acc_id)
                amount_in = float(trans_data["amount"]) if type(trans_data["amount"]) == str else trans_data["amount"]
                balance += amount_in if drcr == "CR" else -amount_in

                # build transaction, lookup txn type
                trans = {"ten_id": data["ten_id"], "customer_account_id": acc_id, "transaction_type": trans_type, "transaction_code": transaction_code, "description": trans_data["description"], "amount": trans_data["amount"], "date": trans_data["date"], "drcr": drcr, "balance": balance, "user_id": data["user_id"]}

                cus_tra = CustomerTransactions()
                cus_tra.fill(trans)
                CrudCustomerTransactions(db).create(cus_tra)
                # now update account
                cus_acc = CrudCustomerAccount(db).get_by_id(acc_id)
                cus_acc.balance = balance
                cus_acc.last_transaction_amount = trans_data["amount"]
                cus_acc.last_transaction_date = trans_data["date"]
                cus_acc.last_transaction_type = trans_type

            db.commit()
        except Exception as xxx:
            error = process_exception(xxx)
            result["error"] = error
            db.rollback()
        return result
