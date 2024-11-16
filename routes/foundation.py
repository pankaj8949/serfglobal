from flask import Blueprint, render_template

foundation_bp = Blueprint("foundation", __name__)

@foundation_bp.route("/foundation")
def Foundation():
    return render_template("screens/foundation/foundation.html")

@foundation_bp.route("/management-team")
def ManagementTeam():
    return render_template("screens/foundation/management_team.html")

@foundation_bp.route("/messages")
def Messages():
    return render_template("screens/foundation/messages.html")