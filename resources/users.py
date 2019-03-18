
import copy

import config

#_seq = 1

class User:
    _seq = 0
    def __init__(self, name, email):
        User._seq += 1
        self._id = str(User._seq)
        self._name = name
        self._email = email

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email

    def __str__(self):
        return '[id={}, name={}, email={}]'.format(self.id, self.name, self.email)

USERS = [
    User('john', 'john@doe.com'),
    User('jane', 'jane@doe.com'),
    User('joe', 'joe@smith.com')
    ]

def list_users():
    return copy.deepcopy(USERS)

def create_user(name, email):
    USERS.append(User(name, email))

def get_user(id):
    users = list([u for u in USERS if u.id == id])
    return users[0] if len(users) > 0 else None

def delete_user(id):
    indices = [i for i,u in enumerate(USERS) if u.id == id]
    if len(indices) > 0:
        idx = indices[0]
        USERS.pop(idx)

def update_user(id, name, email):
    users = list([u for u in USERS if u.id == id])
    if len(users) > 0:
        users[0].name = name
        users[0].email = email




