import os
import json
from typing import Collection
import flask
from flask_sqlalchemy import SQLAlchemy
import gunicorn
import psycopg2
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_mail import Mail, Message
from werkzeug.wrappers import response
from werkzeug.utils import secure_filename
from forms.contact_form import ContactForm
from flask_login import UserMixin, login_user, logout_user, LoginManager, login_required, current_user
import cloudinary.uploader

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')
app.config["MAIL_SERVER"] = os.getenv('MAIL_SERVER')
app.config["MAIL_USERNAME"] = os.getenv('MAIL_USERNAME')
app.config["MAIL_PASSWORD"] = os.getenv('MAIL_PASSWORD')
app.config["MAIL_PORT"] = os.getenv('MAIL_PORT')
app.config['MAIL_USE_SSL'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL_1", 'sqlite:///static/data/horse.db')
mail = Mail(app)

#image cloud storage
cloudinary.config(
    cloud_name=os.getenv('CLOUD_NAME'),
    api_key=os.getenv('CLOUD_KEY'),
    api_secret=os.getenv('CLOUD_SECRET')
)

#database

db = SQLAlchemy(app)



#Database Models
class Horse(db.Model):
    __tablename__ = "horses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    breed = db.Column(db.String, nullable=False)
    height = db.Column(db.Float)
    color = db.Column(db.String)
    sex = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float)
    training = db.Column(db.String, nullable=False)
    saddle_time = db.Column(db.String, nullable=False)
    adoptable = db.Column(db.Boolean, nullable=False)
    bio = db.Column(db.String, nullable=False)
    images = db.relationship('HorseImage', backref='horse_images', lazy=True)

    def __repr__(self):
        return {
            "id": self.id,
            "name": self.name,
            "breed": self.breed,
            "sex": self.sex,
            "age": self.age,
            "price": self.price,
            "training": self.training,
            "saddle_time": self.saddle_time,
            "bio": self.bio,
            "images": self.images
        }


class HorseImage(db.Model):
    __tablename__ = "horse_images"
    id = db.Column(db.String, primary_key=True)
    url = db.Column(db.String, nullable=False)
    comment = db.Column(db.String)
    horse_id = db.Column(db.Integer, db.ForeignKey(
        'horses.id'), nullable=False)

    def __repr__(self):
        return{
            "image": self.url,
            "comment": self.comment
        }


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return{
            "email": self.email,
            "password": self.password
        }


db.create_all()

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Routes

#Home
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template('index.html')

#admin login and sign out
@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    horses = Horse.query.all()
    if request.method == "POST":
        current_user = User.query.filter_by(
            email=request.form["email"]).first()
        if current_user:
            if current_user.password == request.form["password"]:
                login_user(current_user)
                print("logged in")
            else:
                flash("Invalid Password", "error")
        else:
            flash("Not Today", "error")
    return render_template('admin.html', horses=horses)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Successfully Logged Out", "info")
    return redirect(url_for('index'))


#contact me
@app.route("/contact_me", methods=['GET', 'POST'])
def contact_me():
    form = ContactForm()
    if form.validate_on_submit():
        msg = Message("Please Help Message", sender="tim@tccs.tech",
                      recipients=["tim@tccs.tech"])
        msg.body = request.form["message"]
        mail.send(msg)
        return render_template('contact_page/contact_good.html', name=form.name.data, email=form.email.data)
    return render_template('/contact_page/contact.html', form=form)

#Tech Route
@app.route('/workshop')
def workshop():
    message = "this page is in the process of being updated. Thank you for your patience!"
    flash(message.title(), "info")
    return render_template('workshop.html')


#horse routes
@app.route("/horses")
def horses():
    horses = db.session.query(Horse).all()
    return render_template('horses.html', horses=horses)


@app.route("/horses/<id>/<name>")
def horse(name, id):
    selected_horse = Horse.query.filter_by(id=int(id)).first()
    horse_images = HorseImage.query.filter_by(horse_id=int(id)).all()
    return render_template('horse.html', horse=selected_horse, horse_images=horse_images)


@app.route('/add-horse', methods=["POST"])
def add_horse():
    horse = Horse(name=request.form["name"], breed=request.form["breed"], sex=request.form["sex"], age=request.form["age"], price=request.form["price"], training=request.form["training"],
                  saddle_time=request.form["saddle_time"], bio=request.form["bio"], color=request.form["color"], height=request.form['height'])
    db.session.add(horse)
    db.session.commit()
    return redirect(url_for('horses'))


@app.route('/update-horse', methods=["GET", "POST"])
def update_horse():
    if current_user.is_authenticated:
        horse = Horse.query.filter_by(id=request.form["id"]).first()
        horse.name = request.form["name"]
        horse.breed = request.form["breed"]
        horse.sex = request.form["sex"]
        horse.age = request.form["age"]
        horse.price = request.form["price"]
        horse.training = request.form["training"].strip()
        horse.saddle_time = request.form["saddle_time"]
        horse.bio = request.form["bio"]
        horse.color = request.form["color"]
        horse.height = request.form['height']
        horse.adoptable = int(request.form['adoptable'])
        db.session.commit()
        files = request.files.getlist('images')
        comments = request.form.getlist("comment")
        print(files)
        for file in files: 
            print(file) 
            try:         
                image = cloudinary.uploader.upload(file, tag=horse.name)           
                horse_image = HorseImage(
                id=image['public_id'], url=image["url"], comment=comments[files.index(file)], horse_id=horse.id)
                db.session.add(horse_image)
                db.session.commit()
            except cloudinary.exceptions.Error:
                pass
    else:
        flash("You gotta sign in!", "info")
    return redirect(url_for('horse', id=horse.id, name=horse.name))




if __name__ == "__main__":
    app.run(debug=True)
