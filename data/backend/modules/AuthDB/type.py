from collections import namedtuple

Client = namedtuple('Client', ['id', 'name', 'image'])

GoogleUser = namedtuple('GoogleUser', ['id', 'email', 'name', 'locale', 'picture'])