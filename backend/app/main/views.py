import datetime
import requests
import os
import re
import json
from flask import Flask, jsonify, request, abort, make_response
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    jwt_refresh_token_required,
    create_refresh_token,
    get_jwt_identity,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
    decode_token,
)
from app.models import Mentor, Client
from google.oauth2 import id_token
from google.auth.transport.requests import Request
from . import main


@main.route("/", methods=["GET"])
def index():
    return "Welcome to the Move Up CRM Tool backend!"


# Get all mentors from Airtable
@main.route("/mentors", methods=["GET"])
@jwt_required
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

    def getResponse():
        for r in response_json["records"]:
            id_number = r["id"]
            name = r["fields"].get("Name")
            email = r["fields"].get("Move Up Email")
            if name is not None and email is not None:
                m = Mentor(name=name, email=email, id_number=id_number)
                list_of_mentors.append(m.serialize())

    getResponse()
    repeat_pagination(response_json, "Mentors", getResponse)
    return jsonify(list_of_mentors), 200


# Get a mentor by id from Airtable
# SECURITY WARNING: Exposing database id in a URL
@main.route("/mentors/<id>", methods=["GET"])
@jwt_required
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
        return "There is no mentor with this id. Please try again.", 422

    # Create and return object
    mentor = Mentor(name=name, email=email, id_number=id_number)
    return jsonify(mentor.serialize()), 200


# Get a mentor by email from Airtable
@main.route("/mentors/email/<email>", methods=["GET"])
@jwt_required
def get_mentor_by_email(email):
    response = get_mentor_response_by_email(email)
    response_json = response.json()
    # Validation check
    if (response.status_code // 100) != 2:
        return response_json["error"], response.status_code

    error = handleEmailResponse(response_json["records"])
    if error is not None:
        return error, 422

    # Get object's parameters
    id_number = response_json["records"][0]["id"]
    name = response_json["records"][0]["fields"].get("Name")
    email = response_json["records"][0]["fields"].get("Move Up Email")
    if name is None or email is None:
        return "There is no mentor with that email. Please try again.", 422

    # Create and return object
    m = Mentor(name=name, email=email, id_number=id_number)
    return jsonify(m.serialize()), 200


# Get all clients from Airtable
@main.route("/clients", methods=["GET"])
@jwt_required
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

    def getResponse():
        for r in response_json["records"]:
            id_number = r["id"]
            name = r["fields"].get("Name")
            notes = r["fields"].get("Notes")
            email = r["fields"].get("Client Email")
            attachments = r["fields"].get("Attachments")

            if name is not None and email is not None:
                m = Client(
                    name=name,
                    email=email,
                    id_number=id_number,
                    notes=notes,
                    attachments=attachments,
                )
                list_of_clients.append(m.serialize())

    getResponse()
    # Pagination setting that will continue to send requests until all of the records have been retrieved
    repeat_pagination(response_json, "Clients", getResponse)
    return jsonify(list_of_clients), 200


# Get a client from Airtable
# SECURITY WARNING: Exposing database id in a URL
@main.route("/clients/<id>", methods=["GET"])
@jwt_required
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
        return "There is no client with this id. Please try again.", 422

    # Create and return object
    c = Client(
        name=name,
        email=email,
        id_number=id_number,
        notes=notes,
        attachments=attachments,
    )
    return jsonify(c.serialize()), 200


# Get a client from Airtable using client's email
@main.route("/clients/email/<email>", methods=["GET"])
@jwt_required
def get_a_client_from_email(email):
    response = requests.get(
        "https://api.airtable.com/v0/appw4RRMDig1g2PFI/Clients?filterByFormula=SEARCH('{}'".format(
            email
        )
        + ", {Client Email})",
        headers={"Authorization": str(os.environ.get("API_KEY"))},
    )
    # Convert to JSON
    response_json = response.json()

    # Validation check
    if (response.status_code // 100) != 2:
        return response_json["error"], response.status_code

    error = handleEmailResponse(response_json["records"])
    if error is not None:
        return error, 422

    # Get object's parameters
    id_number = response_json["records"][0]["id"]
    name = response_json["records"][0]["fields"].get("Name")
    email = response_json["records"][0]["fields"].get("Client Email")
    notes = response_json["records"][0]["fields"].get("Notes")
    attachments = response_json["records"][0]["fields"].get("Attachments")
    if name is None or email is None:
        return "There is no client with that email. Please try again.", 422

    # Create and return object
    c = Client(
        name=name,
        email=email,
        id_number=id_number,
        notes=notes,
        attachments=attachments,
    )
    return jsonify(c.serialize()), 200


# Gets list of client notes based on clientid or email
@main.route("/notes/<id>", methods=["GET"])
@jwt_required
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


# log in an existing user
@main.route("/auth/login", methods=["POST"])
def login():
    # required in body: email: String
    data = request.get_json(force=True)
    email = data.get("email")
    token = data.get("token")

    try:
        id_token.verify_oauth2_token(token, Request(), os.getenv("GOOGLE_CLIENT_ID"))
    except ValueError:
        return "Invalid Google ID token!", 400

    # get mentor
    response = get_mentor_response_by_email(email)
    response_json = response.json()
    # Validation check
    if (response.status_code // 100) != 2:
        return response_json["error"], response.status_code

    if len(response_json["records"]) == 0:
        return (
            "No Move Up user exists for this Google account! Please add user info to Airtable to log in.",
            400,
        )

    # Get object's parameters
    id_number = response_json["records"][0]["id"]
    name = response_json["records"][0]["fields"].get("Name")
    email = response_json["records"][0]["fields"].get("Move Up Email")

    mentor = Mentor(name=name, email=email, id_number=id_number)

    # create tokens
    access_token = create_access_token(identity=mentor.id_number)
    refresh_token = create_refresh_token(identity=mentor.id_number)

    # set cookies
    resp = jsonify({"user": mentor.serialize()})
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)

    return resp, 200


@main.route("/auth/token/refresh", methods=["POST"])
@jwt_refresh_token_required
def refresh_token():
    # create the new access token
    mentor_id = get_jwt_identity()

    # get mentor
    response = get_mentor_response_by_id(mentor_id)
    response_json = response.json()

    # Validation check
    if (response.status_code // 100) != 2:
        return response_json["error"], response.status_code

    # Get object's parameters
    id_number = response_json["id"]
    name = response_json["fields"].get("Name")
    email = response_json["fields"].get("Move Up Email")
    if name is None or email is None:
        return "There is no mentor with that email. Please try again.", 400

    mentor = Mentor(name=name, email=email, id_number=id_number)

    # create user
    access_token = create_access_token(identity=mentor_id)

    # set the JWT access cookie in the response
    resp = jsonify({"user": mentor.serialize()})
    set_access_cookies(resp, access_token)

    return resp, 200


# log out an existing user
@main.route("/auth/logout", methods=["POST"])
@jwt_required
def logout():
    resp = jsonify("Logged out successfully")
    unset_jwt_cookies(resp)
    return resp, 200


### HELPER METHODS ###


def get_mentor_response_by_email(email):
    return requests.get(
        "https://api.airtable.com/v0/appw4RRMDig1g2PFI/Mentors?filterByFormula=SEARCH('{}'".format(
            email
        )
        + ", {Move Up Email})",
        headers={"Authorization": str(os.environ.get("API_KEY"))},
    )


def get_mentor_response_by_id(id):
    return requests.get(
        "https://api.airtable.com/v0/appw4RRMDig1g2PFI/Mentors/{}".format(id),
        headers={"Authorization": str(os.environ.get("API_KEY"))},
    )


def handleEmailResponse(res):
    if (len(res)) == 0:
        return "No records in this database."
    elif (len(res)) > 1:
        errorMsg = (
            "The email address is associated to "
            + str(len(res))
            + " names. It appears for"
        )
        for i in range(len(res)):
            if i == len(res) - 1:
                errorMsg += " and " + res[i]["fields"].get("Name") + "."
            else:
                errorMsg += " " + res[i]["fields"].get("Name") + ","
        return errorMsg


def repeat_pagination(response_json, userRole, getResponse):
    while "offset" in response_json:
        offset = response_json["offset"]
        response = requests.get(
            (
                "https://api.airtable.com/v0/appw4RRMDig1g2PFI/"
                + userRole
                + "?offset={}"
            ).format(offset),
            headers={"Authorization": str(os.environ.get("API_KEY"))},
        )
        response_json = response.json()
        getResponse()
