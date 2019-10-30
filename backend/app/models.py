import json
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

# create model classes here


class Mentor:

    # contructor
    def __init__(self, name, email, listOfClients):
        self.name = name
        self.email = email
        self.listOfClients = []                 # creates a new empty list for each mentor

    def add_client(self, client):
        self.listOfClients.append(client)
