import datetime
from flask import Flask, jsonify, request, abort, make_response
from . import main
from .. import db


# get all users
@main.route("/", methods=["GET"])
def index():
    return "Hello World!"
