from flask import Blueprint, render_template

payment_bp = Blueprint("payment", __name__)

@payment_bp.route("/make-a-payment")
def MakeAPayment():
    return render_template("pages/payment.html")