from multipart import Headers
from enum import Enum
from datetime import datetime

class ContentType(Enum):
    none = "text/plain"
    plaintext = "text/plain"
    html5 = "text/html"
    json = "application/json"

class Charset(Enum):
    none = "utf-8"
    utf8 = "utf-8"

class StatusCode(Enum):
    cnone = "500 Internal Server Error"
    c200 = "200 OK"
    c201 = "201 Created"
    c202 = "202 Accepted"
    c301 = "301 Moved Permanently"
    c302 = "302 Found"
    c303 = "303 See Other"
    c401 = "401 Unauthorized"
    c403 = "403 Forbidden"
    c409 = "409 Conflict"
    c500 = "500 Internal Server Error"

class Cookie:
    class SameSiteRule(Enum):
        none = 'None'
        lax = 'Lax'
        strict = 'Strict'

    class ExpireTime:
        def __init__(self, year: int, month: int, day: int, hour: int, minute: int, second: int, gmt: int = 0):
            self.year = year
            self.month = month
            self.day = day
            self.hour = hour
            self.minute = minute
            self.second = second
            self.gmt = gmt

        def __str__(self):
            _expire = datetime(self.year, self.month, self.day, self.hour, self.minute, self.second)
            _gmt = ''
            if self.gmt != 0:
                _gmt = ' GMT' + ('+' if self.gmt > 0 else '-') + str(self.gmt)
            return _expire.strftime('%a, %d %b %Y %H:%M:%S') + _gmt
    
    def __init__(self, key: str, value: str, 
                 secure: bool = False,
                 http_only: bool = False,
                 same_site: SameSiteRule | None = None,
                 max_age: int | None = None,
                 expires: ExpireTime | None = None,
                 domain: str | None = None,
                 path: str | None = None,
                 partitioned: bool = False):
        self.key = key
        self.value = value
        self.secure = secure
        self.http_only = http_only
        self.same_site = same_site
        self.expires = expires
        self.max_age = max_age
        self.domain = domain
        self.path = path
        self.partitioned = partitioned

    def __str__(self):
        _cookie = self.key + '=' + self.value
        if self.secure:
            _cookie += '; Secure'
        if self.http_only:
            _cookie += '; HttpOnly'
        if self.max_age:
            _cookie += '; Max-Age=' + str(self.max_age)
        if self.expires and not self.max_age:
            _cookie += '; Expires=' + str(self.expires)
        if self.domain:
            _cookie += '; Domain=' + self.domain
        if self.path:
            _cookie += '; Path=' + self.path
        if self.partitioned:
            _cookie += '; Partitioned'
        if self.same_site:
            _cookie += '; SameSite=' + self.same_site.value
        return _cookie

class header:
    def __init__(self, headers: list | None = None):
        self.data = Headers(headers)
        self.content_type = ContentType.plaintext.value
        self.charset = Charset.utf8.value
        self.cookies = {}

    def getCustomHeader(self, key):
        return self.data[key]

    def setCustomHeader(self, key, value):
        self.data[key] = value

    def setStatusCode(self, _sc: StatusCode | str = StatusCode.cnone):
        if isinstance(_sc, StatusCode):
            self.setCustomHeader('Status', _sc.value)
        else:
            for e in StatusCode:
                _e = e.name.split('c')[1]
                match _sc.lower():
                    case e.value:
                        self.setCustomHeader('Status', e.value)
                    case _e:
                        self.setCustomHeader('Status', e.value)

    def setAccessControlAllowOrigin(self, _loc: str = '*'):
        self.setCustomHeader('Access-Control-Allow-Origin', _loc)

    def setAccessControlAllowCredentials(self, _cred: bool = True):
        self.setCustomHeader('Access-Control-Allow-Credentials', 'true' if _cred else 'false')

    def setAccessControlAllowMethods(self, _meth: list[str] | str = 'GET, POST, PUT, DELETE, OPTIONS'):
        m = ''
        if isinstance(_meth, list):
            for _m in _meth:
                m += _m + ', '
            m = m[:-2]
        else:
            m = _meth
        self.setCustomHeader('Access-Control-Allow-Methods', m)

    def setAccessControlAllowHeaders(self, _head: list[str] | str = 'Content-Type, Authorization'):
        h = ''
        if isinstance(_head, list):
            for _h in _head:
                h += _h + ', '
            h = h[:-2]
        else:
            h = _head
        self.setCustomHeader('Access-Control-Allow-Headers', h)

    def setContentType(self, _type: ContentType | str = ContentType.plaintext):
        if isinstance(_type, ContentType):
            self.content_type = _type.value
        else:
            for e in ContentType:
                match _type.lower():
                    case e.name | e.value:
                        self.content_type = e.value

    def setCharset(self, _cs: Charset | str = Charset.utf8):
        if isinstance(_cs, Charset):
            self.charset = _cs.value
        else:
            for e in Charset:
                match _cs.lower():
                    case e.name | e.value:
                        self.charset = e.value

    def setLocation(self, _loc: str):
        self.setCustomHeader('Location', _loc)

    def setCookie(self, _cookie: Cookie):
        self.cookies[_cookie.key] = _cookie

    def getCookie(self, _key: str) -> Cookie | None:
        return self.cookies.get(_key, None)

    def apply(self):
        self.data["Content-Type"] = self.content_type + '; charset=' + self.charset
        for _cookie in self.cookies:
            #self.data["Set-Cookie"] = str(self.cookies[_cookie])
            self.data.add_header("Set-Cookie", str(self.cookies[_cookie]))
        print(self.data)