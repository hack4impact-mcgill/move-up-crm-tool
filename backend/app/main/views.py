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

# Get all mentors from Airtable
@main.route("/mentors", methods=["GET"])
@main.route("/mentors/", methods=["GET"])
def get_all_mentors():
    response = requests.get(
        "https://api.airtable.com/v0/appw4RRMDig1g2PFI/Mentors",
        headers={"Authorization": str(os.environ.get("API_KEY"))},
    )
    # Convert to JSON
    response_json = response.json()

    # Validation checks
    if (response.status_code // 100) != 2:
        return response_json["error"], response.status_code
    
    # Create and return object
    list_of_mentors = []
    for r in response_json["records"]:
        id_number = r["id"]
        name = r["fields"].get("Name")
        email = r["fields"].get("Move Up Email")
        if name is not None and email is not None:
            m = Mentor(name=name, email=email, id_number=id_number)
            list_of_mentors.append(m.serialize())
    return jsonify(list_of_mentors)


# Get a mentor by id from Airtable
@main.route("/mentors/<id>", methods=["GET"])
@main.route("/mentors/<id>/", methods=["GET"])
def get_mentor_by_id(id):
    response = requests.get(
        "https://api.airtable.com/v0/appw4RRMDig1g2PFI/Mentors/{}".format(id),
        headers={"Authorization": str(os.environ.get("API_KEY"))},
    )
    # Convert to JSON
    response_json = response.json()

    # Validation checks
    if (response.status_code // 100) != 2:
        return response_json["error"], response.status_code
    
    # Get object's parameters
    id_number = response_json["id"]
    name = response_json["fields"].get("Name")
    email = response_json["fields"].get("Move Up Email")
    if name is None or email is None:
        return "There is no mentor with this id. Please try again."
    
    # Create and return object
    mentor = Mentor(name=name, email=email, id_number=id_number)
    return jsonify(mentor.serialize())
        


# Get a mentor by email from Airtable
@main.route("/mentors/email/<email>", methods=["GET"])
@main.route("/mentors/email/<email>/", methods=["GET"])
def get_mentor_by_email(email):
    response = requests.get(
        "https://api.airtable.com/v0/appw4RRMDig1g2PFI/Mentors?filterByFormula=SEARCH('{}'".format(
            email
        )
        + ", {Move Up Email})",
        headers={"Authorization": str(os.environ.get("API_KEY"))},
    )
    # Convert to JSON
    response_json = response.json()

    # Validation check
    if (response.status_code // 100) != 2:
        return response_json["error"], response.status_code
    
    # Get object's parameters
    id_number = response_json["id"]
    name = response_json["fields"].get("Name")
    email = response_json["fields"].get("Move Up Email")
    if name is None or email is None:
        return "There is no mentor with that email. Please try again."
   
    # Create and return object
    m = Mentor(name=name, email=email, id_number=id_number)
    return jsonify(m.serialize())


# Get all clients from Airtable
@main.route("/clients", methods=["GET"])
@main.route("/clients/", methods=["GET"])
def get_all_clients():
    response = requests.get(
        "https://api.airtable.com/v0/appw4RRMDig1g2PFI/Clients",
        headers={"Authorization": str(os.environ.get("API_KEY"))},
    )
    # Convert to JSON
    response_json = response.json()

    # Validation check
    if (response.status_code // 100) != 2:
        return response_json["error"], response.status_code
    
    # Create and return object
    list_of_clients = []
    for r in response_json["records"]:
        id_number = r["id"]
        name = r["fields"].get("Name")
        notes = r["fields"].get("Notes")
        email = r["fields"].get("Client Email")
        attachments = r["fields"].get("Attachments")
        if name is not None and email is not None:
            m = Client(name=name, email=email, id_number=id_number, notes=notes, attachments=attachments)
            list_of_clients.append(m.serialize())
    return jsonify(list_of_clients)

# Get a client from Airtable
@main.route("/clients/<id>", methods=["GET"])
@main.route("/clients/<id>/", methods=["GET"])
def get_a_client(id):
    response = requests.get(
        "https://api.airtable.com/v0/appw4RRMDig1g2PFI/Clients/{}".format(id),
        headers={"Authorization": str(os.environ.get("API_KEY"))},
    )
    # Convert to JSON
    response_json = response.json()

    # Validation check
    if (response.status_code // 100) != 2:
        return response_json["error"], response.status_code
    
    # Get object's parameters
    id_number = response_json["id"]
    name = response_json["fields"].get("Name")
    notes = response_json["fields"].get("Notes")
    email = response_json["fields"].get("Client Email")
    attachments = response_json["fields"].get("Attachments")
    if name is None or email is None:
        return "There is no client with this id. Please try again."

    # Create and return object
    c = Client(name=name, email=email, id_number=id_number, notes=notes, attachments=attachments)
    return jsonify(c.serialize())


# get a client from Airtable using client's email 
@main.route("/clients/email/<email>", methods = ["GET"])
@main.route("/clients/email/<email>/", methods = ["GET"])
def get_a_client_from_email(email): 
    response = requests.get(
        "https://api.airtable.com/v0/appw4RRMDig1g2PFI/Clients?filterByFormula=SEARCH('{}'".format(email) + ", {Client Email})", 
        headers={"Authorization": str(os.environ.get("API_KEY"))},
    )
    # Convert to JSON
    response_json = response.json()

    # Validation check
    if (response.status_code // 100) != 2:
        return response_json["error"], response.status_code
    
    # Get object's parameters
    id_number = response_json["id"]
    name = response_json["fields"].get("Name")
    email = response_json["fields"].get("Client Email")
    notes = response_json["fields"].get("Notes")
    attachments = response_json["fields"].get("Attachments")
    if name is None or email is None:
        return "There is no client with that email. Please try again."
    
    # Create and return object
    c = Client(name=name, email=email, id_number=id_number, notes=notes, attachments=attachments)
    return jsonify(c.serialize())

# get all Volunteers from Airtable
@main.route("/volunteers", methods = ["GET"])
def get_all_volunteers():
    response = requests.get(
        "https://api.airtable.com/v0/appw4RRMDig1g2PFI/Volunteers",
        headers={"Authorization": str(os.environ.get("API_KEY"))},
    )
    # Convert to JSON
    response_json = response.json()

    # Validation check
    if (response.status_code // 100) != 2:
        return response_json["error"], response.status_code
    
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
    # Convert to JSON
    response_json = response.json()

    # Validation check
    if (response.status_code // 100) != 2:
        return response_json["error"], response.status_code
    
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
    # Convert to JSON
    response_json = response.json()

    # Validation check
    if (response.status_code // 100) != 2:
        return response_json["error"], response.status_code
    
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
