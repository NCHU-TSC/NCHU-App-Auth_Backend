import os
import sys
from urllib import parse
from .header import header

def processOptions_CORS(origin: str, method: list[str], headers: list[str]) -> bool:
    if os.getenv("REQUEST_METHOD").upper() == "OPTIONS":
        h = header()
        h.setAccessControlAllowOrigin(origin)
        h.setAccessControlAllowCredentials()
        h.setAccessControlAllowMethods(method)
        h.setAccessControlAllowHeaders(headers)
        h.apply()
        return True
    return False

def fromPOST(qs_like: bool = False) -> dict[str, list[str]] | str:
    if os.getenv("REQUEST_METHOD").upper() == "POST":
        content_length_str = os.getenv("CONTENT_LENGTH")

        if content_length_str and sys.stdin:
            content_length = int(content_length_str)
            return parse.parse_qs(sys.stdin.buffer.read(content_length).decode(encoding='utf-8')) if qs_like else sys.stdin.buffer.read(content_length).decode(encoding='utf-8')

    return ""
    
def fromGET() -> dict[str, list[str]]:
    return parse.parse_qs(os.getenv("QUERY_STRING"))

def fromPUT(qs_like: bool = True) -> dict[str, list[str]] | str:
    if os.getenv("REQUEST_METHOD").upper() == "PUT":
        content_length_str = os.getenv("CONTENT_LENGTH")

        if content_length_str and sys.stdin:
            content_length = int(content_length_str)
            return parse.parse_qs(sys.stdin.buffer.read(content_length).decode(encoding='utf-8')) if qs_like else sys.stdin.buffer.read(content_length).decode(encoding='utf-8')
        
    return {}

def fromCOOKIE() -> dict[str, str]:
    cookies = os.getenv("HTTP_COOKIE")
    return parseCookie(cookies)

def parseCookie(cookie_str: str) -> dict[str, str]:
    cookies = {}
    if cookie_str:
        for cookie in cookie_str.split('; '):
            key, value = cookie.split('=', 1)
            cookies[key] = value
    return cookies