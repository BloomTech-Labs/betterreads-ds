from flask import Flask, jsonify, Blueprint

from ..route_tools.nyt import NYT

nyt = Blueprint("nyt", __name__)


@nyt.route("/nyt/fiction", methods=["GET"])
def nyt_fiction():
    nyt = NYT()
    return nyt.get("combined-print-and-e-book-fiction")


@nyt.route("/nyt/nonfiction", methods=["GET"])
def nyt_nonfiction():
    nyt = NYT()
    return nyt.get("combined-print-and-e-book-nonfiction")
