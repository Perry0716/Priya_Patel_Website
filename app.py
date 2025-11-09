from flask import Flask, render_template, request, redirect, flash, url_for

app = Flask(__name__)
app.secret_key = "your_secret_key"

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
            flash("Thank you for reaching out! I will get back to you soon.", "success")
            return redirect(url_for("contact"))
    return render_template("contact.html", page="contact")

@app.route("/resume")
def resume():
    return render_template("resume.html", page="resume")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", page="404"), 404

if __name__ == "__main__":
    app.run(debug=True)
