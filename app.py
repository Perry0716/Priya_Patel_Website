from flask import Flask, render_template, request, redirect, flash, url_for

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a secure env variable in production

@app.route("/")
def home():
    return render_template("index.html", page="home")

@app.route("/about")
def about():
    return render_template("about.html", page="about")

@app.route("/work")
def work():
    # Sample projects for placeholder
    projects = [
        {
            "title": "Visualizing & Forecasting Stocks",
            "description": "An analytical dashboard leveraging Python, data visualization libraries, and Jupyter Notebook to model and predict stock trends.",
            "image": "project1.jpg",
            "category": "Data Science",
            "skills": ["Python", "Jupyter", "Pandas", "Matplotlib"]
        },
        {
            "title": "Aurora Fashion E-Commerce Website",
            "description": "End-to-end responsive e-commerce platform developed with Flask, SQL, HTML, CSS, and JavaScript. Features include dynamic product displays, interactive filters, shopping cart, wishlists, and user auth.",
            "image": "project2.jpg",
            "category": "Web Development",
            "skills": ["Flask", "SQL", "HTML", "CSS", "JavaScript"]
        },
        {
            "title": "Sales Performance Dashboard",
            "description": "Interactive Tableau dashboard for analyzing company sales KPIs. Enables strategic planning via real-time metrics visualization.",
            "image": "project1.jpg",
            "category": "Analytics",
            "skills": ["Tableau", "Excel"]
        },
        {
            "title": "Portfolio Website",
            "description": "Personal portfolio website built with Bootstrap, HTML/CSS/JS, and SQL for showcasing professional achievements.",
            "image": "project2.jpg",
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
        
        # Simple server-side validation
        if not name or not email or not message:
            flash("All fields are required.", "error")
        elif "@" not in email or "." not in email:
            flash("Please enter a valid email address.", "error")
        else:
            # Here you would handle the form,
            # e.g., send an email or save to database.
            flash("Thank you for reaching out! I will get back to you soon.", "success")
            return redirect(url_for("contact"))
    return render_template("contact.html", page="contact")

@app.route("/resume")
def resume():
    return render_template("resume.html", page="resume")

# Error handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", page="404"), 404

if __name__ == "__main__":
    app.run(debug=True)

