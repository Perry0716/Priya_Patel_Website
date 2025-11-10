
from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# Database configuration
if os.environ.get('DATABASE_URL'):
    # Production (Heroku)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://')
else:
    # Local development
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # In production, hash this!
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create tables
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html", page="home")

@app.route("/about")
def about():
    return render_template("about.html", page="about")

@app.route("/work")
def work():
    projects = [
        {
            "title": "Visualizing & Forecasting Stocks",
            "description": "Dashboard for analyzing and predicting stock trends with Python, Jupyter, and Matplotlib.",
            "image": "stock.jpg",
            "category": "Data Science",
            "skills": ["Python", "Jupyter", "Pandas", "Matplotlib"]
        },
        {
            "title": "Aurora Fashion E-Commerce Website",
            "description": "Full-stack e-commerce site (Flask, SQL, HTML, CSS, JS) with wishlist, filters, and dynamic content.",
            "image": "ecomm.jpg",
            "category": "Web Development",
            "skills": ["Flask", "SQL", "HTML", "CSS", "JavaScript"]
        },
        {
            "title": "Sales Performance Dashboard",
            "description": "Interactive Tableau dashboard for KPIs and sales analytics.",
            "image": "tableau.jpg",
            "category": "Analytics",
            "skills": ["Tableau", "Excel"]
        },
        {
            "title": "Portfolio Website",
            "description": "Personal portfolio (Bootstrap, HTML, CSS, JS, SQL) for project & resume showcase.",
            "image": "portfolio.jpg",
            "category": "Web Development",
            "skills": ["Bootstrap", "HTML", "CSS", "JavaScript", "SQL"]
        }
    ]
    categories = sorted({proj['category'] for proj in projects})
    return render_template("work.html", page="work", projects=projects, categories=categories)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()
        
        if not name or not email or not message:
            flash("All fields are required.", "error")
        elif "@" not in email or "." not in email:
            flash("Please enter a valid email address.", "error")
        else:
            # Save to database
            contact_msg = ContactMessage(name=name, email=email, message=message)
            db.session.add(contact_msg)
            db.session.commit()
            flash("Thank you for reaching out! I will get back to you soon.", "success")
            return redirect(url_for("contact"))
    return render_template("contact.html", page="contact")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        
        if not username or not email or not password:
            flash("All fields are required to join the club!", "error")
        elif "@" not in email:
            flash("That email looks suspicious... 🤔", "error")
        elif len(password) < 6:
            flash("Password too short! We need at least 6 characters for security.", "error")
        elif User.query.filter_by(username=username).first():
            flash("That username is taken! Try being more creative. 😉", "error")
        elif User.query.filter_by(email=email).first():
            flash("This email is already registered. Having déjà vu? Try logging in!", "error")
        else:
            # In production, hash the password!
            user = User(username=username, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            flash("Welcome to the club! 🎉 You can now log in.", "success")
            return redirect(url_for("login"))
    return render_template("signup.html", page="signup")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        
        if not username or not password:
            flash("Both fields are required to enter the secret chamber! 🔐", "error")
        else:
            user = User.query.filter_by(username=username).first()
            if user and user.password == password:  # In production, hash comparison!
                session['user_id'] = user.id
                session['username'] = user.username
                flash(f"Welcome back, {user.username}! 🚀", "success")
                return redirect(url_for("dashboard"))
            else:
                flash("Wrong credentials! Are you sure you're not a robot? 🤖", "error")
    return render_template("login.html", page="login")

@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        flash("Please log in to access your dashboard!", "error")
        return redirect(url_for("login"))
    return render_template("dashboard.html", page="dashboard")

@app.route("/logout")
def logout():
    username = session.get('username', 'Mystery Person')
    session.clear()
    flash(f"Goodbye, {username}! Come back soon! 👋", "success")
    return redirect(url_for("home"))

@app.route("/resume")
def resume():
    return render_template("resume.html", page="resume")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", page="404"), 404

if __name__ == "__main__":
    app.run(debug=True)
