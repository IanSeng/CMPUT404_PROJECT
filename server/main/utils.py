"""main user model Configuration
This file is used to store static varible and enums
to be used for main user model
"""

from enum import Enum

# TODO: Add host once we have the host IP
HOST = ""

class UserType(Enum):
    superuser = 'superuser'
    author = 'author'