import json
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

# create model classes here


class Mentor:

    # constructor
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def serialize(self):
        return {"name": self.name, "email": self.email}


class Client:

    # constructor
    def __init__(self, name, notes, attachments):
        self.name = name
        self.notes = notes
        self.attachments = attachments

    def serialize(self):
        return {
            "name": self.name,
            "notes": self.notes,
            "attachments": self.attachments
        }

class Volunteer:

    #constructor
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def serialize(self):
        return {
            "name": self.name,
            "email": self.email
        }
