import datetime
import requests
import os
import re
from flask import Flask, jsonify, request, abort, make_response
from app.models import Mentor, Client, Volunteer
from app.email import send_email
from . import main

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
    if response.status_code == 200:
        list_of_mentors = []
        response_json = response.json()
        for r in response_json["records"]:
            name = r["fields"].get("Name")
            email = r["fields"].get("Move Up Email")
            if name is not None and email is not None:
                m = Mentor(name=name, email=email)
                list_of_mentors.append(m.serialize())
        return jsonify(list_of_mentors)
    else:
        return "There are no mentors in the database.", response.status_code


# get a mentor by id from Airtable
@main.route("/mentors/<id>", methods=["GET"])
def get_mentor_by_id(id):
    response = requests.get(
        "https://api.airtable.com/v0/appw4RRMDig1g2PFI/Mentors/{}".format(id),
        headers={"Authorization": str(os.environ.get("API_KEY"))},
    )
    if response.status_code == 200:
        response_json = response.json()
        name = response_json["fields"].get("Name")
        email = response_json["fields"].get("Move Up Email")
        if name is not None and email is not None:
            mentor = Mentor(name=name, email=email)
            return jsonify(mentor.serialize())
    else:
        return "This mentor does not exist in the database.", response.status_code


# get a mentor by email from Airtable
@main.route("/mentors/email/<email>", methods=["GET"])
def get_mentor_by_email(email):
    response = requests.get(
        "https://api.airtable.com/v0/appw4RRMDig1g2PFI/Mentors?filterByFormula=SEARCH('{}'".format(
            email
        )
        + ", {Move Up Email})",
        headers={"Authorization": str(os.environ.get("API_KEY"))},
    )
    if response.status_code == 200:
        response_json = response.json()
        for r in response_json["records"]:
            name = r["fields"].get("Name")
            email = r["fields"].get("Move Up Email")
            if name is not None and email is not None:
                m = Mentor(name=name, email=email)
                return jsonify(m.serialize())
    else:
        return "There is no mentor with that email, please try again.", response.status_code


# get all clients from Airtable
@main.route("/clients", methods=["GET"])
def get_all_clients():
    response = requests.get(
        "https://api.airtable.com/v0/appw4RRMDig1g2PFI/Clients",
        headers={"Authorization": str(os.environ.get("API_KEY"))},
    )
    if response.status_code == 200:
        list_of_clients = []
        response_json = response.json()
        for r in response_json["records"]:
            name = r["fields"].get("Name")
            notes = r["fields"].get("Notes")
            email = r["fields"].get("Client Email")
            attachments = r["fields"].get("Attachments")
            if name is not None and email is not None:
                m = Client(name=name, email=email, notes=notes, attachments=attachments)
                list_of_clients.append(m.serialize())
        return jsonify(list_of_clients)
    else:
        return "There are no clients in the database.", response.status_code


# get a client from Airtable
@main.route("/clients/<id>", methods=["GET"])
def get_a_client(id):
    response = requests.get(
        "https://api.airtable.com/v0/appw4RRMDig1g2PFI/Clients/{}".format(id),
        headers={"Authorization": str(os.environ.get("API_KEY"))},
    )
    if response.status_code == 200:
        response_json = response.json()
        client = []
        name = response_json["fields"].get("Name")
        notes = response_json["fields"].get("Notes")
        email = response_json["fields"].get("Client Email")
        attachments = response_json["fields"].get("Attachments")
        if name is not None and email is not None:
            m = Client(name=name, email=email, notes=notes, attachments=attachments)
            client.append(m.serialize())
            return jsonify(client)
    else:
        return "This client does not exist in the database.", response.status_code


# get a client from Airtable using client's email 
@main.route("/clients/email/<email>", methods = ["GET"])
def get_a_client_from_email(email): 
    response = requests.get(
        "https://api.airtable.com/v0/appw4RRMDig1g2PFI/Clients?filterByFormula=SEARCH('{}'".format(email) + ", {Client Email})", 
        headers={"Authorization": str(os.environ.get("API_KEY"))},
    )
    if response.status_code == 200:
        list_of_clients = []
        response_json = response.json()
        for r in response_json["records"]:
            name = r["fields"].get("Name")
            email = r["fields"].get("Client Email")
            notes = r["fields"].get("Notes")
            attachments = r["fields"].get("Attachments")
            if name is not None and email is not None:
                m = Client(name=name, email=email, notes=notes, attachments=attachments)
                list_of_clients.append(m.serialize())
                return jsonify(list_of_clients)
    else: 
        return "There is no client with that email, please try again.", response.status_code

# get all Volunteers from Airtable
@main.route("/volunteers", methods = ["GET"])
def get_all_volunteers():
    response = requests.get(
        "https://api.airtable.com/v0/appw4RRMDig1g2PFI/Volunteers",
        headers={"Authorization": str(os.environ.get("API_KEY"))},
    )
    if response.status_code == 200: 
        list_of_volunteers = []   
        response_json = response.json()
        for r in response_json["records"]:
            name = r["fields"].get("Name")
            notes = r["fields"].get("Notes")
            email = r["fields"].get("Volunteer Email")
            attachments = r["fields"].get("Attachments")
            if name is not None and email is not None:
                m = Volunteer(name=name, email=email, notes=notes, attachments=attachments)
                list_of_volunteers.append(m.serialize())
        return jsonify(list_of_volunteers)
    else:
        return "There are no volunteers in the database.", response.status_code

# get a volunteer from Airtable
@main.route("/volunteers/<id>", methods = ["GET"])
def get_a_volunteer(id):
    response = requests.get(
        "https://api.airtable.com/v0/appw4RRMDig1g2PFI/Volunteers/{}".format(id),
        headers={"Authorization": str(os.environ.get("API_KEY"))},
    )
    if response.status_code == 200:
        response_json = response.json()
        volunteer = []
        name = response_json["fields"].get("Name")
        notes = response_json["fields"].get("Notes")
        email = response_json["fields"].get("Volunteer Email")
        attachments = response_json["fields"].get("Attachments")
        if name is not None and email is not None:
            m = Volunteer(name=name, email=email, notes=notes, attachments=attachments)
            volunteer.append(m.serialize())
            return jsonify(volunteer)
    else:
        return "This volunteer does not exist in the database", response.status_code

# get a volunteer from Airtable using volunteer's email 
@main.route("/volunteers/email/<email>", methods = ["GET"])
def get_volunteer_by_email(email): 
    response = requests.get(
        "https://api.airtable.com/v0/appw4RRMDig1g2PFI/Volunteers?filterByFormula=SEARCH('{}'".format(email) + ", {Volunteer Email})", 
        headers={"Authorization": str(os.environ.get("API_KEY"))},
    )
    print(response.json())
    if response.status_code == 200:
        list_of_volunteers = []
        response_json = response.json()
        for r in response_json["records"]:
            name = r["fields"].get("Name")
            email = r["fields"].get("Volunteer Email")
            notes = r["fields"].get("Notes")
            attachments = r["fields"].get("Attachments")
            if name is not None and email is not None:
                m = Client(name=name, email=email, notes=notes, attachments=attachments)
                list_of_volunteers.append(m.serialize())
                return jsonify(list_of_volunteers)
    else: 
        return "There is no volunteer with that email, please try again.", response.status_code







# Gets list of client notes based on clientid or email
@main.route("/notes/<id>", methods=["GET"])
def get_client_notes(id):
    # Regex used to check if string input is an email address
    regex = "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    email_input = re.search(regex, id)

    regex = "^[A-Za-z0-9_()]{17}$"
    id_input = re.search(regex, id)

    if email_input:
        # id is an email. Collect client notes by email
        response = requests.get(
            "https://api.airtable.com/v0/appw4RRMDig1g2PFI/Clients?filterByFormula=SEARCH('{}'".format(
                id
            )
            + ", {Client Email})",
            headers={"Authorization": str(os.environ.get("API_KEY"))},
        )
    elif id_input:
        # id is an id. Collect notes by id
        response = requests.get(
            "https://api.airtable.com/v0/appw4RRMDig1g2PFI/Clients/{}".format(id),
            headers={"Authorization": str(os.environ.get("API_KEY"))},
        )
    else:
        # Return failure
        return "Bad id/email", 400

    if response.status_code == 200:
        response_json = response.json()

        notes = []
        if email_input:
            for r in response_json["records"]:
                notes.append(r["fields"].get("Notes"))
        else:
            notes.append(response_json["fields"]["Notes"])
        # Return accepted status
        return jsonify(notes), 200

    # Failed to read json
    return "Failed to get client's notes", 400


# send emails by calling send_mail from email.py
@main.route("/send-email", methods=["POST"])
def send_mail():
    # get email recipients and subject from the POST request
    data = request.get_json(force=True)
    recipients = data.get("recipients")
    subject = data.get("subject")

    if recipients is None or subject is None:
        abort(400, "Recipient(s) and subject cannot be empty")

    send_email(recipients, subject)
    return "message sent!"
