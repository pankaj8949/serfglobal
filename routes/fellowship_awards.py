from flask import Blueprint, render_template

fellowship_awards_bp = Blueprint("fellowship_awards", __name__)

@fellowship_awards_bp.route("/national-awards")
def NationalAwards():
    return render_template("screens/fellowship-awards/national_awards.html")

@fellowship_awards_bp.route("/global-awards")
def GlobalAwards():
    return render_template("screens/fellowship-awards/global_awards.html")

@fellowship_awards_bp.route("/application")
def Application():
    return render_template("screens/fellowship-awards/application.html")
