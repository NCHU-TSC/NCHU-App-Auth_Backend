import random
import string
import hashlib

def take_column(table: list[tuple], column_num: int) -> list:
    _column = []
    for i in table:
        _column.append(i[column_num])

    return _column

def random_token(length: int = 64) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def salting_password(password: str, salt_len: int = 16) -> tuple[str, str]:
    salt = random_token(salt_len)
    return password + salt, salt

def hash_password(password: str) -> str:
    return hashlib.sha3_512(password.encode()).hexdigest()

def hash_password_with_salt(password: str) -> tuple[str, str]:
    c, s = salting_password(password)
    return hash_password(c), s

def verify_password(password: str, hashed: str, salt: str) -> bool:
    return hash_password(password + salt) == hashed