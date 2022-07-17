import requests
import os
from flask import flash, redirect, url_for
from werkzeug.utils import secure_filename
from .utilconstants import TEMPLATE_COLUMN_HEADERS
import csv
from sqlalchemy.orm import sessionmaker
from services import CustomerService
from crud import CrudImportlogs, CrudTennants
from datetime import datetime
import time


class UtilityService:
    def find_template_name(self, col_header):
        data_name = ""
        # define static list sets, first column in col_header is template name
        # loop through
        for col in TEMPLATE_COLUMN_HEADERS:
            # print(col)
            # print(col_header)
            if col == col_header.lower():
                tokens = col.split("#")
                data_name = tokens[0]
                break

        return data_name

    def import_template(self, filename):
        with open(filename, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            data = []
            for row in csv_reader:
                data.append(dict(row))

        return data

    def load_bulk_data(self, db: sessionmaker, template_name, filename, created_by):
        print("load data file ==================== ",
              template_name, filename, created_by)
        result = {"error": "", "data": ""}
        data = []
        with open(filename, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                data.append(dict(row))

        if len(data) == 0:
            result["error"] = "Error: No data found in template"
            return result

        # get keys as array
        col_list = [*data[0]]

        print("load data col list ==================== ", col_list)
        print("load data size ==================== ", len(data))

        otherpart = ','.join(col_list[1:])
        col_head = f"{col_list[0]}#{otherpart}"
        tname = self.find_template_name(col_head)
        print("load data col data name ==================== ", tname)

        if len(tname) == 0:
            result["error"] = "ERROR: Invalid template submitted."
        elif tname.lower() == template_name.lower():
            # check for dupliicty, consistence for name and ten_id
            nrow = 0
            fname = data[0][col_list[0]]
            temp_ten_id = data[0][col_list[1]]

            print("temp_ten_id ================= ", temp_ten_id)

            nsize = len(data)
            print("file name id ============================ ", fname)
            for item in data:
                nrow += 1
                if item[col_list[0]] != fname:
                    result["error"] = f"ERROR: Invalid template id, ROW - {nrow}, {item[col_list[0]]}"
                    return result
                if item[col_list[1]] != temp_ten_id:
                    result["error"] = f"ERROR: Invalid ten_id , ROW - {nrow}, {item[col_list[1]]}"
                    return result

            # do we have a valid tendant
            ten_data = CrudTennants(db).get_by_id(temp_ten_id)
            if not ten_data:
                result["error"] = f"ERROR: Invalid ten_id  {temp_ten_id}."
                return result

            ten_id = ten_data.id
            # check duplicate log
            print(
                "CrudImportlogs(db).get_by_name(ten_id, fname) ============================ ", ten_id, fname)
            log = CrudImportlogs(db).get_by_name(ten_id, fname)
            if log:
                result["error"] = f"ERROR: File with id  {fname} already imported."
                return result

            logrow = {
                "ten_id": data[0]["ten_id"],
                "file_id": fname,
                "size": nsize,
                "path": filename,
                "created_by": data[0]["ten_id"]
            }
            result = self.handle_bulk_insert(db, tname, data, logrow)

            # if successful, log it
        else:
            result["error"] = f"ERROR: Invalid template submitted {template_name}"

        return result

    def handle_bulk_insert(self, db: sessionmaker, data_name, data, logdata):
        print("================== handle_bulk_insert")
        result = {"error": "", "data": ""}
        if data_name == "customers":
            result = CustomerService().add_customer_bulk(db, data, logdata)
        elif data_name == "customer_transactions":
            result = CustomerService().add_customer_transaction_bulk(db, data, logdata)
        else:
            result["error"] = f"ERROR: Import operation for {data_name} not supported"
        return result

    def allowed_upload_file(self, filename):
        ALLOWED_EXTENSIONS = set(
            ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def upload_file(self, upload_dir, request):
        # check if the post request has the file part
        if 'file' not in request.files:
            #flash('No file part')
            return "ERROR: No file part specified."
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            #flash('No selected file')
            return "ERROR: No file was selected for upload."
        if file and self.allowed_upload_file(file.filename):
            print("file======================= ", file.filename)
            filename = secure_filename(file.filename)
            print("file======================= 2 ", filename)
            file.save(os.path.join(upload_dir, filename))
            print("file======================= uploaded 3 ", filename)

            return ""
        return "ERROR: Noaction taken, Unknown error."

    def upload_template_data(self, db: sessionmaker, request):
        result = {
            "error": "",
            "data": ""
        }
        upload_dir = "data/temp"
        # check if the post request has the file part
        if 'file' not in request.files:
            #flash('No file part')
            return {
                "error": "ERROR: No file part specified.",
                "data": ""
            }
        file = request.files['file']
        template_name = request.form['template_name']
        created_by = request.form['created_by']
        print("template_name =============== = ", template_name)
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            #flash('No selected file')
            return {
                "error": "ERROR: No file was selected for upload.",
                "data": ""
            }
        if file and self.allowed_upload_file(file.filename):
            print("file======================= ", file.filename)
            filename = secure_filename(file.filename)
            print("file======================= 2 ", filename)
            file.save(os.path.join(upload_dir, filename))
            print("file======================= uploaded 3 ", filename)

            # now import the data
            file_path = f"{upload_dir}/{filename}"
            result = self.load_bulk_data(
                db, template_name, file_path, created_by)

        return result
