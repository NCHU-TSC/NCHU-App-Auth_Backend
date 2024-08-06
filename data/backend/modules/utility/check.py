import re

def check_email(email: str) -> bool:
    return re.match(r'^\w+@\w+\.\w+$', email) is not None

def check_nchu_email(email: str) -> bool: # *@*.nchu.edu.tw
    return re.match(r'^\w+@.*\.nchu\.edu\.tw$', email) is not None

def check_image_encoded_by_base64(image: str) -> bool:
    return re.match(r'^data:image/\w+;base64,[A-Za-z0-9+/]+={0,2}$', image) is not None