from flask import Blueprint, render_template

journals_bp = Blueprint("journals", __name__)

@journals_bp.route("/current-journal")
def CurrentJournals():
    return render_template("screens/journals/current_journal.html")

@journals_bp.route("/upcoming-journals")
def UpcomingJournals():
    return render_template("screens/journals/upcoming_journals.html")

