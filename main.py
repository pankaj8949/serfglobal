from flask import Flask, render_template, request, redirect, send_file, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from routes.foundation import foundation_bp
from routes.journals import journals_bp
from routes.conferences import conferences_bp   
from routes.fellowship_awards import fellowship_awards_bp
from routes.membership import membership_bp
from routes.contact import contact_bp
from routes.payment import payment_bp
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

if not url or not key:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY environment variables")

supabase = create_client(url, key)

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

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # Get form data
        fullname = request.form.get('fullname')
        username = request.form.get('username')
        email = request.form.get('email')
        gender = request.form.get('gender')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Basic validation
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('register'))

        try:
            # Check if user exists
            user = supabase.table('supa_user').select('*').eq('email', email).execute()
            if user.data:
                flash('Email already registered', 'error')
                return redirect(url_for('register'))

            # Create new user
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            user_data = {
                'fullname': fullname,
                'username': username,
                'email': email,
                'gender': gender,
                'password': hashed_password
            }
            
            result = supabase.table('supa_user').insert(user_data).execute()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
            return redirect(url_for('register'))

    return render_template("auth/register.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form.get('username_or_email')
        password = request.form.get('password')
        remember = request.form.get('remember-me')

        try:
            user = supabase.table('supa_user')\
                .select('*')\
                .or_(f'email.eq.{username_or_email},username.eq.{username_or_email}')\
                .execute()
            
            if user.data and check_password_hash(user.data[0]['password'], password):
                # Store user info in session
                session['user_id'] = user.data[0]['id']
                session['username'] = user.data[0]['username']
                
                if remember:
                    session.permanent = True

                flash('Login successful!', 'success')
                return redirect(url_for('Home'))
            else:
                flash('Invalid username/email or password', 'error')
                return redirect(url_for('login'))

        except Exception as e:
            print(f"Login error: {str(e)}")  # Debug print
            flash(f'An error occurred: {str(e)}', 'error')
            return redirect(url_for('login'))

    return render_template("auth/login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/sitemap.xml')
def sitemap():
    return send_file('static/sitemap.xml', mimetype='application/xml')

@app.route('/robots.txt')
def robots():
    return send_file('static/robots.txt', mimetype='text/plain')

@app.route('/favicon.ico')
def favicon():
    return send_file('static/favicon.ico', mimetype='image/x-icon')

@app.route('/profile')
@login_required
def profile():
    return f"Hello, {session['username']}!"

if __name__ == "__main__":
    app.run(debug=True)