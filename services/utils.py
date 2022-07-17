
def process_exception(exp: Exception):
    error = str(exp)
    print("catch ==========================================", error)
    msg = "Error: General error."
    if error.find("UniqueViolation") > 0 or error.find("duplicate key") > 0:
        msg = "ERROR: Attempt to add a duplicate item rejected."
    elif error.find("ForeignKeyViolation") > 0 or error.find("foreign key constraint") > 0:
        msg = "ERROR: Attempt to add orphan record was rejected."
    else:
        # we do this to identify more exceptions in the ui and build the list
        msg = f"{msg} - {error}"

    return msg
