import json
from werkzeug.security import generate_password_hash, check_password_hash

# create model classes here
class User:
     # constructor
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def serialize(self):
        return {
            "name": self.name, 
            "email": self.email
            }

class Mentor(User):
    pass


class Client(User):

    # constructor
    def __init__(self, name, email, notes, attachments):
        super().__init__(name, email)
        self.notes = notes
        self.attachments = attachments

    def serialize(self):
        return {
            "name": self.name,
            "email": self.email,
            "notes": self.notes,
            "attachments": self.attachments
        }

class Donor(User):
    pass
