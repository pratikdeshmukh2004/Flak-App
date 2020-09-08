from flask import Flask, jsonify, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import Form 
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length, AnyOf

app = Flask(__name__)
db = SQLAlchemy(app)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config['SECRET_KEY'] = 'DontTellAnyone'


class UserForm(Form):
	firstname = StringField('firstname', validators=[InputRequired()])
	lastname = StringField('lastname', validators=[InputRequired()])

# creating Table name User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50)) 
    date_created = db.Column(db.DateTime, default=datetime.now)

# Home page route
@app.route("/")
def users():
    # for getting all users from users table
    users = User.query.all()
    userslist = []
    for user in users:
        userslist.append({"firstname": user.firstname, "lastname": user.lastname, "joining": user.date_created, "id": user.id})
    return render_template("index.html", users=userslist)

@app.route("/new", methods=["POST", "GET"])
def new_user():
    if request.method == "GET":
        form=UserForm()
        return render_template("new.html", form=form)
    user = User(firstname=request.form["firstname"], lastname=request.form["lastname"])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for("users"))

@app.route("/get/<int:id>")
def get_user(id):
    user = User.query.filter_by(id=id).first()
    return render_template("show.html", user=user)

@app.route("/delete/<int:id>")
def delete_user(id):
    user = User.query.filter_by(id=id).first()
    if user is not None:
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("users"))
    else:
        return redirect(url_for("users"))

@app.route("/eidit/<int:id>", methods=["POST", "GET"])
def edit_user(id):
    user = User.query.filter_by(id=id).first()
    if request.method == "GET":
        form=UserForm()
        return render_template("edit.html", form=form, user=user)
    user.firstname = request.form["firstname"]
    user.lastname = request.form["lastname"]
    db.session.commit()
    return redirect(url_for("users"))