import json
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

# create model classes here


class Mentor:

    # contructor
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def serialize(self):
        return {"name": self.name, "email": self.email}
