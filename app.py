from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent

app = Flask(__name__)
app.config["SECRET_KEY"] = "PTC_TRADERS_SECRET_2026_CHANGE_THIS"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "PTC@2026ChangeMe"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{BASE / 'ptc_traders.db'}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Inquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(150), nullable=False)
    person = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(40), nullable=False)
    quantity = db.Column(db.String(80), nullable=False)
    specification = db.Column(db.String(250))
    location = db.Column(db.String(180), nullable=False)
    requirement_date = db.Column(db.String(30))
    message = db.Column(db.Text)
    status = db.Column(db.String(30), default="New")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class FarmerRegistration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(40), nullable=False)
    village = db.Column(db.String(150), nullable=False)
    area = db.Column(db.String(50), nullable=False)
    expected_production = db.Column(db.String(80))
    message = db.Column(db.Text)
    status = db.Column(db.String(30), default="New")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/inquiry", methods=["POST"])
def inquiry():
    item = Inquiry(
        company=request.form["company"].strip(),
        person=request.form["person"].strip(),
        phone=request.form["phone"].strip(),
        quantity=request.form["quantity"].strip(),
        specification=request.form.get("specification","").strip(),
        location=request.form["location"].strip(),
        requirement_date=request.form.get("date","").strip(),
        message=request.form.get("message","").strip()
    )
    db.session.add(item)
    db.session.commit()
    flash("Your inquiry has been received. PTC Traders will contact you shortly.", "success")
    return redirect(url_for("home") + "#inquiry")

@app.route("/farmer-registration", methods=["POST"])
def farmer_registration():
    item = FarmerRegistration(
        name=request.form["name"].strip(),
        phone=request.form["phone"].strip(),
        village=request.form["village"].strip(),
        area=request.form["area"].strip(),
        expected_production=request.form.get("expected_production", "").strip(),
        message=request.form.get("message", "").strip()
    )
    db.session.add(item)
    db.session.commit()
    flash("Farmer registration received. PTC Traders will contact you shortly.", "success")
    return redirect(url_for("home") + "#contract-farming")

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if session.get("admin_logged_in"):
        return redirect(url_for("admin"))
    if request.method == "POST":
        if request.form.get("username", "").strip() == ADMIN_USERNAME and request.form.get("password", "") == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("admin"))
        flash("Wrong username or password.", "error")
    return render_template("login.html")

@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("admin_login"))

@app.route("/admin")
def admin():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    inquiries = Inquiry.query.order_by(Inquiry.created_at.desc()).all()
    farmers = FarmerRegistration.query.order_by(FarmerRegistration.created_at.desc()).all()
    return render_template("admin.html", inquiries=inquiries, farmers=farmers)

@app.route("/admin/status/<int:item_id>", methods=["POST"])
def update_status(item_id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    item = Inquiry.query.get_or_404(item_id)
    item.status = request.form["status"]
    db.session.commit()
    return redirect(url_for("admin"))

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
