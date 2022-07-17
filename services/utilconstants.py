
TEMPLATE_COLUMN_HEADERS = [
    "customers#ten_id,customer_name,customer_type,address,location,country,primary_phone,secondary_phone,email,tax_no,account1,account2,account3,account4",
    "customer_account#ten_id,customer_ref,account_no,account_type,account_priority,device_id",
    "customer_transactions#ten_id,account_no,transaction_type,description,amount,date",
    "device#ten_id,serial_number,device_type,barcode"
]

DR_TRANSACTIONS = ["WITHDRAW", "PENALTY", "CHARGE", "BILL"]
CR_TRANSACTIONS = ["DEPOSIT", "REFUND", "REWARD", "GIFT"]
