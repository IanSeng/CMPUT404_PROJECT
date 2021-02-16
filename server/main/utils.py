from enum import Enum

# TODO: Add host once we have the host IP
HOST = ""

class UserType(Enum):
    superuser = 'superuser'
    author = 'author'