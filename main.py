from flask import Flask, render_template
from routes.foundation import foundation_bp
from routes.journals import journals_bp
from routes.conferences import conferences_bp   
from routes.fellowship_awards import fellowship_awards_bp
from routes.membership import membership_bp
from routes.contact import contact_bp
from routes.payment import payment_bp

app = Flask(__name__)
app.secret_key = 'serfglobal_2024secretkey'

# Register Blueprints
app.register_blueprint(foundation_bp)
app.register_blueprint(journals_bp)
app.register_blueprint(conferences_bp)
app.register_blueprint(fellowship_awards_bp)
app.register_blueprint(membership_bp)
app.register_blueprint(contact_bp)
app.register_blueprint(payment_bp)
@app.errorhandler(404)
def PageNotFound(e):
    return render_template("pages/404.html"), 404

@app.route("/")
def Home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)