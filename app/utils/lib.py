
def map_to_dict(obj, fields):
    return {field: getattr(obj, field) for field in fields}

def map_list_to_dicts(obj_list, fields):
    return [map_to_dict(obj, fields) for obj in obj_list]

def schem_to_dict(obj, schema):
    return schema.dump(obj)

def to_dict_list(obj_list, schema):
    return [schem_to_dict(obj, schema) for obj in obj_list]