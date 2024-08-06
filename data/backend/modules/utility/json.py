import json
import decimal
from datetime import datetime, date, time

def regularize(v):
    _result = None

    if isinstance(v, dict):
        _result = regularize_d(v)
    elif isinstance(v, tuple):
        _result = regularize_l(v)
    elif isinstance(v, list):
        _result = regularize_l(v)
    elif isinstance(v, bytearray):
        _result = int.from_bytes(v)
    elif isinstance(v, bytes):
        _result = int.from_bytes(v)
    elif isinstance(v, datetime):
        _result = "{}/{}/{} {}:{}:{}:{}".format(v.year, v.month, v.day, v.hour, v.minute, v.second, v.microsecond)
    elif isinstance(v, date):
        _result = "{}/{}/{}".format(v.year, v.month, v.day)
    elif isinstance(v, time):
        _result = "{}:{}:{}:{}".format(v.hour, v.minute, v.second, v.microsecond)
    elif isinstance(v, decimal.Decimal):
        _result = int(v)
    else:
        _result = v
    
    return _result

def regularize_l(__list: tuple | list):
    _tmp = []
    for l in __list:
        _tmp.append(regularize(l))

    return _tmp

def regularize_d(__dict: dict) -> dict:
    _tmp = {}
    for k, v in __dict.items():
        _tmp[k] = regularize(v)

    return _tmp

def toJSON(__dict: dict) -> str:
    return json.dumps(regularize(__dict))

def fromJSON(__json: str) -> dict:
    return json.loads(__json)