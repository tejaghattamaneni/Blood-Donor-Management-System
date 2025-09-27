from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "supersecretkey"  # required for session

# Database config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///donors.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Donor model
class Donor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    blood_group = db.Column(db.String(10), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    location = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

# Home page → donor form
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        blood = request.form["blood"]
        mobile = request.form["mobile"]
        location = request.form["location"]

        donor = Donor(name=name, blood_group=blood, mobile=mobile, location=location)
        db.session.add(donor)
        db.session.commit()

        # Mark user as registered in session
        session["registered"] = True
        session["username"] = name

        return f"Donor {name} saved successfully! <br><a href='/search'>Go to Search</a>"
    return render_template("index.html")

# Search donors by location and blood group
@app.route("/search", methods=["GET", "POST"])
def search():
    if not session.get("registered"):
        return redirect(url_for("index"))  # only allow registered users

    donors = []
    if request.method == "POST":
        location = request.form["location"]
        blood = request.form["blood"]
        donors = Donor.query.filter_by(location=location, blood_group=blood).all()

    return render_template("search.html", donors=donors)
if __name__ == "__main__":
    app.run(debug=True)
