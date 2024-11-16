from flask import Blueprint, render_template

membership_bp = Blueprint("membership", __name__)

@membership_bp.route("/membership-benifits")
def MembershipBenifits():
    return render_template("screens/membership/m_benifits.html")

@membership_bp.route("/membership-details")
def MembershipDetails():
    return render_template("screens/membership/m_details.html")

@membership_bp.route("/online-application")
def OnlineApplication():
    return render_template("screens/membership/online_appc.html")

@membership_bp.route("/list-of-life-members")
def ListOfLifeMembers():
    return render_template("screens/membership/lolm.html")