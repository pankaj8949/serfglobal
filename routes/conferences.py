from flask import Blueprint, render_template

conferences_bp = Blueprint("conferences", __name__)

@conferences_bp.route("/past-conferences")
def PastConferences():
    return render_template("screens/conferences/past_conf.html")

@conferences_bp.route("/upcoming-conferences")
def UpcomingConferences():
    return render_template("screens/conferences/upcoming_conf.html")