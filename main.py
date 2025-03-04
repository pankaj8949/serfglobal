from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from routes.foundation import foundation_bp
from routes.journals import journals_bp
from routes.conferences import conferences_bp   
from routes.fellowship_awards import fellowship_awards_bp
from routes.membership import membership_bp
from routes.contact import contact_bp
from routes.payment import payment_bp

db = SQLAlchemy()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:serfglobalauth@db.uyanofddigzsbpxarrci.supabase.co:5432/postgres" 

db.init_app(app)

class SupaUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    gender = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

with app.app_context():
    db.create_all()  
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

        # Check if username already exists
        existing_user = SupaUser.query.filter_by(username=username).first()
        if existing_user:
            flash('This user already exists, please try to login', 'error')
            return redirect(url_for('register'))

        # Check if email already exists
        existing_email = SupaUser.query.filter_by(email=email).first()
        if existing_email:
            flash('This email is already registered, please use a different email', 'error')
            return redirect(url_for('register'))

        # Create new user with hashed password
        new_user = SupaUser(
            fullname=fullname,
            username=username,
            email=email,
            gender=gender,
            password=generate_password_hash(password, method='pbkdf2:sha256')
        )
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'error')
            return redirect(url_for('register'))

    return render_template("auth/register.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember-me')

        # Find user by username
        user = SupaUser.query.filter_by(username=username).first()

        # Check if user exists and password is correct
        if user and check_password_hash(user.password, password):
            # Store user info in session
            session['user_id'] = user.id
            session['username'] = user.username
            
            # If remember me is checked, set permanent session
            if remember:
                session.permanent = True

            flash('Login successful!', 'success')
            return redirect(url_for('Home'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))

    return render_template("auth/login.html")

# Add a logout route
@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    return redirect(url_for('login'))

# Optional: Add a decorator to protect routes that require login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Example of using the login_required decorator:
@app.route('/profile')
@login_required
def profile():
    return f"Hello, {session['username']}!"

if __name__ == "__main__":
    app.run(debug=True)