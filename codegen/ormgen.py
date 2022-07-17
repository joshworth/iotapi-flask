import csv
import yaml
import sys


class OrmWizard:
    indent = ""
    indent_level2 = ""
    conf = None

    PYTYPES = {"Integer": "int", "String": "str", "DateTime": "datetime", "Boolean": "bool", "Float": "float", "TransactionState": "TransactionState"}
    PYTYPES_SCHEMA = {"Integer": "int", "String": "str", "DateTime": "datetime", "Boolean": "bool", "Float": "float", "TransactionState": "str"}

    def __init__(self, mode):
        # load config
        fconf = self.load_conf()
        conf_key = "orm_prod" if mode == "prod" else "orm"
        self.conf = fconf[conf_key]
        print(f"conf ========== mode : {mode} ::: {conf_key}", self.conf)
        self.indent = self.conf["indent_width"] * " "  # number of single spaces
        self.indent_level2 = 2 * self.indent

    def load_conf(self):
        print("Loading app config .... ")
        data = None
        with open("conf.yml", "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

        print("... Done Loading app config")

        return data

    def import_template(self, filename):
        data = []
        with open(filename, mode="r") as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=",")
            for row in csv_reader:
                data.append(dict(row))

        # organise object hierachy
        modules = []
        models = []
        schema = {}
        cur_module = ""
        cur_model = ""
        for item in data:
            # detect module change, create module key
            if item["module"] not in modules and item["module"] != "":
                cur_module = item["module"]
                modules.append(item["module"])
                schema[cur_module] = {}

            full_model = f"{cur_module}#{item['model']}"
            # detect model change, create model key for module
            if item["model"] != "" and full_model not in models:
                cur_model = item["model"]
                models.append(full_model)
                schema[cur_module][cur_model] = {}

            # print("schema ======== 1  ", schema)
            # create field as whole row
            schema[cur_module][cur_model][item["field"]] = item

        return schema

    def get_object_name(self, schema_name):
        # split by _, capitalize first letter, combine
        tokens = schema_name.split("_")
        obj_name = ""
        for tok in tokens:
            obj_name += tok[0].upper() + tok[1:]
        return obj_name

    def get_py_default(self, def_val):
        if def_val == "utcnow":
            return "datetime.datetime.utcnow"
        elif def_val.lower() == "false" or def_val.lower() == "true":
            return def_val[0].upper() + def_val[1:].lower()
        else:
            return def_val

    def build_field(self, field_name, schema):
        code_lines = []
        field_code = ""
        relation_code = ""
        col_type = schema["type"]
        pare_part = f"{col_type}"
        # primary key
        if schema["pk"] == "y":
            pare_part = f"{pare_part}, primary_key=True, index=True"
        else:
            if col_type == "TransactionState":
                pare_part = f'Enum({col_type}), name="{field_name}_state"'
            if schema["fk"] != "":
                fk = schema["fk"]
                pare_part = f'{pare_part}, ForeignKey("{fk}")'
                lhs_name = fk.split(".")[0]
                obj_name = self.get_object_name(lhs_name)
                backref = ""
                if schema["backref"] != "":
                    backref = schema["backref"]
                    backref = f', backref="{backref}"'
                backpop = ""
                if schema["back_populates"] != "":
                    backpop = schema["back_populates"]
                    backpop = f', back_populates="{backpop}"'
                relation_code = f'{lhs_name} = relationship("{obj_name}"{backref}{backpop})'
                # check if backref, backpop
            if schema["nullable"] != "":
                pare_part += ", nullable=" + ("True" if schema["nullable"] == "y" else "False")
            if schema["default"] != "":
                # if text, default in quotes
                default = self.get_py_default(schema["default"])
                if col_type == "String":
                    default = f'"{default}"'
                pare_part += f", default={default}"
            if schema["onupdate"] != "":
                onupdate = self.get_py_default(schema["onupdate"])
                if onupdate == "utcnow":
                    onupdate = "datetime.datetime.utcnow"

                pare_part += f", onupdate={onupdate}"

        # now we have column code
        field_code = f"{field_name} = Column({pare_part})"

        code_lines.append(field_code)
        code_lines.append(relation_code)
        return code_lines

    def get_model_head(self):
        _indent = self.indent
        _indent_indent = self.indent_level2
        ilines = []
        ilines.append("\nimport hashlib")
        ilines.append("\nfrom sqlalchemy import create_engine, ForeignKey, Table, Column, Integer, Float, String, Boolean, UniqueConstraint, Numeric, DateTime, UniqueConstraint")
        ilines.append("\nfrom sqlalchemy.orm import relationship")
        ilines.append("\nfrom flask import Flask, jsonify")
        ilines.append("\nimport datetime")
        ilines.append("\nfrom sqlalchemy_serializer import SerializerMixin")
        ilines.append("\nfrom urllib import parse")
        ilines.append("\nfrom base import Base")

        return ilines

    def get_schema_imports(self):
        ilines = []
        ilines.append("\nfrom datetime import date, datetime, time, timedelta")
        ilines.append("\nfrom typing import Optional, List")
        ilines.append("\nfrom pydantic import BaseModel")
        return ilines

    def gen_crud_class(self, model_name):
        mname = self.get_object_name(model_name)
        _indent = self.indent
        _indent_indent = self.indent_level2

        lines = []
        lines.append("\n")
        lines.append(f"\nclass _Crud{mname}():")
        lines.append(f"\n{_indent}db: sessionmaker")
        lines.append(f"\n\n{_indent}def __init__(self, db: sessionmaker):")
        lines.append(f"\n{_indent_indent}self.db = db")

        lines.append(f"\n\n{_indent}def create(self, data: {mname}):")
        lines.append(f"\n{_indent_indent}self.db.add(data)")
        lines.append(f"\n{_indent_indent}return data")

        lines.append(f"\n\n{_indent}def edit(self, data):")
        lines.append(f'\n{_indent_indent}{model_name}_data: {mname} = self.db.query({mname}).get(data["id"])')
        lines.append(f"\n{_indent_indent}if {model_name}_data:")
        lines.append(f"\n{_indent_indent}{_indent}{model_name}_data.fill(data)")
        lines.append(f"\n{_indent_indent}return {model_name}_data")

        lines.append(f"\n\n{_indent}def get_all(self, ten_id):")
        lines.append(f"\n{_indent_indent}{model_name}_data = self.db.query({mname}).filter({mname}.ten_id == ten_id)")
        lines.append(f"\n{_indent_indent}return {model_name}_data.all() if {model_name}_data else None")

        lines.append(f"\n\n{_indent}def get_by_id(self, {model_name}_id: int):")
        lines.append(f"\n{_indent_indent}{model_name}_data = self.db.query({mname}).get({model_name}_id)")
        lines.append(f"\n{_indent_indent}return {model_name}_data")

        lines.append("\n")
        return lines

    def get_crud_code(self, module_name, module_schema):
        crud_lines = []
        crud_lines.append("\nfrom sqlalchemy.orm import sessionmaker, load_only")

        return_lines = []

        # import models
        class_lines = []
        sc_lines = []
        mline = f"\nfrom models import "
        models_list = [*module_schema]
        i = 0
        import_line = f"\nfrom ._crud_{module_name} import "
        for mod in models_list:
            mline += (", " if i > 0 else "") + self.get_object_name(mod)
            mname = self.get_object_name(mod)
            import_line += (", " if i > 0 else "") + f"_{mname}"
            clines = self.gen_crud_class(mod)
            class_lines.extend(clines)
            i += 1

        crud_lines.append(mline)
        crud_lines.extend(sc_lines)
        crud_lines.extend(class_lines)
        crud_lines.append("\n")

        return crud_lines, import_line

    def get_models_code(self, module_schema):

        _indent = self.indent
        _indent_indent = self.indent_level2
        model_code = []
        # import libraries, may need clean up later
        # import reference models, not part of the module
        # build class code according to fields
        models_list = [*module_schema]
        print("models ================= ", models_list)
        import_line = "\nfrom .models import "
        mcount = 0
        for model in models_list:
            print("Code for +++++++++++++++++++++++", model)
            model_name = self.get_object_name(model)
            import_line += (", " if mcount > 0 else "") + model_name
            model_code.append(f"\n\nclass {model_name}(Base, SerializerMixin):")
            model_code.append(f'\n{_indent}__tablename__ = "{model}"')
            pare_part = ""
            model_schema = module_schema[model]
            field_list = [*model_schema]
            flines = []
            i = 0
            for field in field_list:
                pare_part += (", " if i > 0 else "") + f'"{field}"'
                fschema = module_schema[model][field]
                # print(fschema)
                lines = self.build_field(field, fschema)
                flines.extend(lines)
                i += 1

            model_code.append(f"\n{_indent}serialize_only = ({pare_part})")
            for line in flines:
                if line != "":
                    model_code.append(f"\n{_indent}{line}")

            print(model_code)

            model_code.append(f"\n\n{_indent}def fill(self, _dict):")
            model_code.append(f"\n{_indent_indent}self.__dict__.update(_dict)")

            mcount += 1

        return model_code, import_line

    def gen_schema_class(self, name, suffix, model_schema):
        lines = []
        field_list = [*model_schema]
        model_name = self.get_object_name(name)
        class_def = f"\n\nclass {model_name}{suffix}(BaseModel):"
        lines.append(class_def)
        for field in field_list:
            fschema = model_schema[field]
            # print("fschema === ", fschema)

            ftype = self.PYTYPES_SCHEMA[fschema["type"]]
            tcode = ""
            fdefinition = fschema[suffix.lower()]
            if fdefinition == "y":
                tcode = ftype
            elif fdefinition == "m":
                tcode = f"Optional[{ftype}]"

            if tcode != "":
                fline = f"\n{self.indent}{field}: {tcode}"
                lines.append(fline)
        return lines

    def get_schemas_code(self, module_schema):
        schemas_code = []
        imp = self.get_schema_imports()
        schemas_code.extend(imp)
        models_list = [*module_schema]
        for model in models_list:
            # create
            clines = self.gen_schema_class(model, "Create", module_schema[model])
            schemas_code.extend(clines)

            # update
            ulines = self.gen_schema_class(model, "Update", module_schema[model])
            schemas_code.extend(ulines)
            # indb
            ilines = self.gen_schema_class(model, "InDB", module_schema[model])
            schemas_code.extend(ilines)
        return schemas_code

    def get_random_function_code(self, field_type):
        func_map = {"String": "utils.random_lower_string()", "Integer": "utils.random_with_N_digits(3)", "Float": "utils.random_float_with_N_digits(3)", "email": "utils.random_email()", "DateTime": "utils.date_time_now()", "TransactionState": "TransactionState.ACTIVE.value"}
        return func_map[field_type]

    def gen_create_obj(self, local_indent, model_name, model_schema):
        rlines = []
        mname = self.get_object_name(model_name)
        field_list = [*model_schema]
        def_lines = []
        obj_in_name = f"{model_name}_in"
        create_params = ""
        assert_lines = []
        assert_lines.append(f"\n{local_indent}assert {model_name}")

        assert_fields = []

        i = 0
        for field in field_list:
            fschema = model_schema[field]
            if fschema["create"] == "y" or fschema["create"] == "m":
                rhs = ""
                if fschema["fk"] != "":
                    tokens = fschema["fk"].split(".")
                    def_lines.append(f"\n{local_indent}{tokens[0]} = utils.create_random_{tokens[0]}(db=db)")
                    rhs = f"{tokens[0]}.id"

                elif fschema["test_default"] != "":
                    rhs = self.get_py_default(fschema["test_default"])
                    if fschema["type"] == "String":
                        rhs = f'"{rhs}"'
                else:
                    rhs = self.get_random_function_code(fschema["type"])
                def_lines.append(f"\n{local_indent}{field} = {rhs}")
                create_params += (", " if i > 0 else "") + f"{field} = {field}"
                assert_fields.append(field)
                i += 1
        rlines.extend(def_lines)
        obj_line = f"\n{local_indent}{obj_in_name} = schemas.{mname}Create({create_params})"
        creator = f"\n{local_indent}creator = utils.random_lower_string()"
        rlines.append(creator)
        rlines.append(obj_line)
        crudline = f"\n{local_indent}{model_name} = crud.{model_name}.create(db=db, obj_in={obj_in_name}, creator=creator)"
        rlines.append(crudline)
        return rlines, assert_fields

    def gen_test_create(self, model_name, model_schema):
        test_lines = []
        test_lines.append(f"\n\ndef test_create_{model_name}(db: Session) -> None:")
        rlines, afields = self.gen_create_obj(self.indent, model_name, model_schema)
        test_lines.extend(rlines)
        assert_lines = []
        assert_lines.append(f"\n{self.indent}assert {model_name}")
        for field in afields:
            assert_lines.append(f"\n{self.indent}assert {model_name}.{field} == {field}")
        test_lines.extend(assert_lines)
        return test_lines

    def gen_test_get(self, model_name, model_schema):
        test_lines = []
        test_lines.append(f"\n\ndef test_get_{model_name}(db: Session) -> None:")

        rlines, afields = self.gen_create_obj(self.indent, model_name, model_schema)
        test_lines.extend(rlines)
        # read line
        indbname = f"{model_name}_indb"
        crud_line = f"\n{self.indent}{indbname} = crud.{model_name}.get(db=db, id={model_name}.id)"
        test_lines.append(crud_line)
        assert_lines = []
        assert_lines.append(f"\n{self.indent}assert {indbname}")
        for field in afields:
            assert_lines.append(f"\n{self.indent}assert {model_name}.{field} == {field}")
        test_lines.extend(assert_lines)
        return test_lines

    def gen_test_get_multi(self, model_name, model_schema):
        test_lines = []
        test_lines.append(f"\n\ndef test_get_multi_{model_name}(db: Session) -> None:")
        rlines, afields = self.gen_create_obj(self.indent_level2, model_name, model_schema)
        test_lines.append(f"\n{self.indent}for _ in range(3):")
        test_lines.extend(rlines)

        # read line
        indbname = f"{model_name}_list"
        crud_line = f"\n{self.indent}{indbname} = crud.{model_name}.get_multi(db=db)"
        test_lines.append(crud_line)

        assert_lines = []
        assert_lines.append(f"\n{self.indent}assert {indbname}")
        assert_lines.append(f"\n{self.indent}assert len({indbname}) >= 3")
        test_lines.extend(assert_lines)
        return test_lines

    def get_tests_code(self, module_name, module_schema):
        tlines = []
        tlines.append("\nfrom sqlalchemy.orm import Session")
        tlines.append("\nfrom app import crud, schemas, models")
        tlines.append("\nfrom app.tests import utils")
        tlines.append("\nfrom app.models import TransactionState")

        # group model code together
        models_list = [*module_schema]
        for model in models_list:
            # create
            clines = self.gen_test_create(model, module_schema[model])
            tlines.extend(clines)
            # get
            glines = self.gen_test_get(model, module_schema[model])
            tlines.extend(glines)
            # get multi
            gmlines = self.gen_test_get_multi(model, module_schema[model])
            tlines.extend(gmlines)

        return tlines

    def get_utils_code(self, module_name, module_schema):

        tlines = []
        imports = []
        tlines.append("\nfrom sqlalchemy.orm import Session")
        tlines.append("\nfrom app import crud, schemas, models")
        tlines.append("\nfrom app.tests import utils")
        tlines.append("\nfrom app.models import TransactionState")

        utils = []
        model_init = f"\nfrom .{module_name} import"
        schema_inits = []
        crud_init = f"\nfrom .{module_name} import"

        # group model code together
        models_list = [*module_schema]
        i = 0
        for model in models_list:
            utils.append(f"\n\ndef create_random_{model}(db: Session):")
            # create
            clines, flist = self.gen_create_obj(self.indent, model, module_schema[model])
            # add return
            clines.append(f"\n{self.indent}return {model}")
            utils.extend(clines)

            mname = self.get_object_name(model)
            schema_inits.append(f"\nfrom .{module_name} import {mname}Create, {mname}InDB, {mname}Update")
            model_init += (", " if i > 0 else " ") + self.get_object_name(model)
            crud_init += (", " if i > 0 else " ") + model
            i += 1
        tlines.extend(imports)
        tlines.extend(utils)

        tlines.append('\n\n"""')
        tlines.append("\n# models.__init__.py")
        tlines.append(model_init)
        tlines.append("\n")
        tlines.append("\n# crud.__init__.py")
        tlines.append(crud_init)
        tlines.append("\n")
        tlines.append("\n# schema.__init__.py")
        tlines.extend(schema_inits)
        tlines.append('\n\n"""')
        return tlines

    def generate_service_code(self, module_name, module_schema):
        _indent = self.indent
        _indent_indent = f"{self.indent}{self.indent}"
        _indent_indent_indent = f"{_indent_indent}{_indent}"
        tlines = []
        tlines.append("\nfrom .utils import process_exception")
        tlines.append("\nfrom sqlalchemy.orm import sessionmaker")
        tlines.append("\nfrom datetime import datetime")

        cimports = "\nfrom crud import "
        mimports = "\nfrom models import "
        models_list = [*module_schema]
        i = 0
        for model in models_list:
            mname = self.get_object_name(model)
            cimports += (", " if i > 0 else "") + f"Crud{mname}"
            mimports += (", " if i > 0 else "") + f"{mname}"
            i += 1
        tlines.append(cimports)
        tlines.append(mimports)

        mdname = self.get_object_name(module_name)
        service_init = f"\nfrom .{module_name} import {mdname}"
        tlines.append(f"\n\nclass {mdname}Service:")
        tlines.append(f"\n{_indent}def list_{module_name}(self, db: sessionmaker, ten_id: int):")
        res_obj = '{"error": "", "data": []}'
        tlines.append(f"\n{_indent_indent}result = {res_obj}")
        tlines.append(f"\n{_indent_indent}try:")
        tlines.append(f"\n{_indent_indent_indent}pass")
        tlines.append(f"\n{_indent_indent}except Exception as xxx:")
        tlines.append(f"\n{_indent_indent_indent}error = process_exception(xxx)")
        tlines.append(f'\n{_indent_indent_indent}result["error"] = error')
        tlines.append(f"\n{_indent_indent_indent}db.rollback()")
        tlines.append(f"\n{_indent_indent}return result")

        tlines.append(f"\n\n{_indent}def lookup_{module_name}(self, db: sessionmaker, data):")
        tlines.append(f"\n{_indent_indent}result = {res_obj}")
        tlines.append(f"\n{_indent_indent}try:")
        tlines.append(f"\n{_indent_indent_indent}pass")
        tlines.append(f"\n{_indent_indent}except Exception as xxx:")
        tlines.append(f"\n{_indent_indent_indent}error = process_exception(xxx)")
        tlines.append(f'\n{_indent_indent_indent}result["error"] = error')
        tlines.append(f"\n{_indent_indent_indent}db.rollback()")
        tlines.append(f"\n{_indent_indent}return result")

        tlines.append(f"\n\n{_indent}def add_{module_name}(self, db: sessionmaker, data):")
        tlines.append(f"\n{_indent_indent}result = {res_obj}")
        tlines.append(f"\n{_indent_indent}try:")
        tlines.append(f"\n{_indent_indent_indent}pass")
        tlines.append(f"\n{_indent_indent}except Exception as xxx:")
        tlines.append(f"\n{_indent_indent_indent}error = process_exception(xxx)")
        tlines.append(f'\n{_indent_indent_indent}result["error"] = error')
        tlines.append(f"\n{_indent_indent_indent}db.rollback()")
        tlines.append(f"\n{_indent_indent}return result")

        return tlines, service_init

    def write_code(self, filename, lines):
        # overwrite existing, dont append
        with open(filename, "w") as code_file:
            code_file.writelines(lines)

    def run(self):
        filename = self.conf["template_file"]
        print(f"generating orm code ******************************************** source: {filename}")
        code = {}
        schema = self.import_template(filename)
        # print(schema)
        modules_list = [*schema]

        models_code = []
        ormconf = self.conf

        service_init = []
        model_init = []
        crud_init = []

        for modu in modules_list:
            code[modu] = {}
            code[modu]["models"], code[modu]["models_init"] = self.get_models_code(schema[modu])
            model_init.extend(code[modu]["models_init"])

            code[modu]["schemas"] = self.get_schemas_code(schema[modu])

            code[modu]["crud"], code[modu]["crud_init"] = self.get_crud_code(modu, schema[modu])
            crud_init.extend(code[modu]["crud_init"])
            code[modu]["test"] = self.get_tests_code(modu, schema[modu])
            code[modu]["utils"] = self.get_utils_code(modu, schema[modu])
            code[modu]["service"], code[modu]["service_init"] = self.generate_service_code(modu, schema[modu])
            service_init.extend(code[modu]["service_init"])

        # write code
        model_lines = []
        model_lines.extend(self.get_model_head())

        for mod in modules_list:
            model_lines.extend(code[mod]["models"])
            # crud
            fname = f"{ormconf['crud_path']}/_crud_{mod}.py"
            self.write_code(fname, code[mod]["crud"])

            # service stub
            fname = f"{ormconf['service_path']}/_{mod}service.py"
            self.write_code(fname, code[mod]["service"])

        # single  files
        # models
        # print(model_lines)
        fname = f"{ormconf['models_path']}/models.py"
        self.write_code(fname, model_lines)
        fname = f"{ormconf['models_path']}/__init__.py"
        self.write_code(fname, model_init)
        fname = f"{ormconf['crud_path']}/__init__.py"
        self.write_code(fname, crud_init)
        fname = f"{ormconf['service_path']}/__init__.py"
        self.write_code(fname, service_init)

        print(f"Done generating orm code ****************** ")


def launch(params):
    mode = "test"
    nargs = len(params)
    if nargs > 1 and (params[1] == "prod" or params[1] == "test"):
        mode = params[1]
    elif nargs > 1:
        print("ERROR: Unknown commandline parameter {}".format(params[1]))
        return

    orm = OrmWizard(mode)
    orm.run()


launch(sys.argv)