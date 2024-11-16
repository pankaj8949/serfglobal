from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.mail_service import mail_service

contact_bp = Blueprint("contact", __name__)

@contact_bp.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':

        name = request.form.get("name", "")
        email = request.form.get("email", "")
        subject = request.form.get("subject", "")
        message = request.form.get("message", "")

        if not all([name, email, subject, message]):
            flash("Please fill all the fields", "error")
            return redirect(url_for("contact.contact"))
        
        mail_service.send_email(name, email, subject, message)
        flash("Message sent successfully", "success")
        return redirect(url_for("contact.contact"))
    
    return render_template("pages/contact.html")