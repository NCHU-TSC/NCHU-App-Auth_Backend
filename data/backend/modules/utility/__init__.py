from . import *

def value_dearrayify(__dict: dict) -> dict:
    for key, value in __dict.items():
        if isinstance(value, list):
            if len(value) == 1:
                __dict[key] = value[0]
    return __dict


def filtering_get(__dict: dict, key: str, valid_values: list, default=None):
    value = __dict.get(key, default)
    if value not in valid_values:
        return default
    return value

def transpose2D(matrix: list[list]) -> list[list]:
    return [[row[i] for row in matrix] for i in range(len(matrix[0]))]

def labeling(matrix: list[list], labels: list) -> list[dict]:
    return [dict(zip(labels, row)) for row in matrix]

def bin2bool(b: bytes) -> bool:
    return False if b == b'0' else True

def console_mode():
    while True:
        try:
            exec(input('>>> '))
        except KeyboardInterrupt:
            print('KeyboardInterrupt')
            break