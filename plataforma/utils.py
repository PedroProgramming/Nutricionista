def validate_fields_patient(*args):
    return all(arg.strip() != "" for arg in args)