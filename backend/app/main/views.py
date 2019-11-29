import datetime
import requests
import os
from flask import Flask, jsonify, request, abort, make_response
from app.models import Mentor, Client
from . import main
from .. import db


# get all users
@main.route("/", methods=["GET"])
def index():
    return "Hello World!"


# get all mentors from Airtable
@main.route("/mentors", methods=["GET"])
def get_all_mentors():
    response = requests.get(
        "https://api.airtable.com/v0/appw4RRMDig1g2PFI/Mentors",
        headers={"Authorization": str(os.environ.get("API_KEY"))},
    )
    response_json = response.json()

    list_of_mentors = []
    for r in response_json["records"]:
        name = r["fields"].get("Name")
        email = r["fields"].get("Move Up Email")
        if name is not None and email is not None:
            m = Mentor(name=name, email=email)
            list_of_mentors.append(m.serialize())
    return jsonify(list_of_mentors)


# get all clients from Airtable
@main.route("/clients", methods=["GET"])
def get_all_clients():
    response = requests.get(
        "https://api.airtable.com/v0/appw4RRMDig1g2PFI/Clients",
        headers={"Authorization": str(os.environ.get("API_KEY"))},
    )
    response_json = response.json()

    list_of_clients = []
    for r in response_json["records"]:
        name = r["fields"].get("Name")
        notes = r["fields"].get("Notes")
        attachments = r["fields"].get("Attachments")
        if name is not None:
            m = Client(name=name, notes=notes, attachments=attachments)
            list_of_clients.append(m.serialize())
    return jsonify(list_of_clients)


# get a client from Airtable 
@main.route("/clients/<id>", methods=["GET"])
def get_a_client(id):
    response = requests.get( 
        "https://api.airtable.com/v0/appw4RRMDig1g2PFI/Clients/{}".format(id),
        headers={"Authorization": str(os.environ.get("API_KEY"))},
    )
    print(response.status_code)
    if response.status_code == 200: 
        response_json = response.json()
        client = []
        name = response_json["fields"].get("Name")
        notes = response_json["fields"].get("Notes")
        attachments = response_json["fields"].get("Attachments")
        if name is not None:
            m = Client(name=name, notes=notes, attachments=attachments)
            client.append(m.serialize())
            return jsonify(client)
    else: 
        return "This client does not exist in the database."


# get a client from Airtable using client's email 
@main.route("/clients/email/<email>", methods = ["GET"])
def get_a_client_from_email(email): 
    response = requests.get(
        "https://api.airtable.com/v0/appw4RRMDig1g2PFI/Clients?filterByFormula=SEARCH('{}'".format(email) + ", {Client Email})", 
        headers={"Authorization": str(os.environ.get("API_KEY"))},
    )
    response_json = response.json()

    list_of_clients = []
    for r in response_json["records"]:
        name = r["fields"].get("Name")
        notes = r["fields"].get("Notes")
        attachments = r["fields"].get("Attachments")
        if name is not None:
            m = Client(name=name, notes=notes, attachments=attachments)
            list_of_clients.append(m.serialize())
            return jsonify(list_of_clients)
    else: 
        return "There is no client with that email, please try again."




