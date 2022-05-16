from ipaddress import ip_address
import os
import json
from typing import Collection
import flask
from flask_sqlalchemy import SQLAlchemy
import gunicorn
import psycopg2
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_mail import Mail, Message
from forms.contact_form import ContactForm





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

# Routes

#Home
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template('index.html')


#contact me
@app.route("/contact_me", methods=['GET', 'POST'])
def contact_me():
    form = ContactForm()
    if form.validate_on_submit():
        if request.form["address"]:
            pass
        else:
            msg = Message("Please Help Message", sender="tim@tccs.tech",
                        recipients=["tim@tccs.tech"])
            sender = request.form["email"]
            message = request.form["message"]
            ip_address = request.form["ip_address"]
            msg.body = f"From:{sender}\nIP ADDRESS: {ip_address}\n\n{message}"
            mail.send(msg)      
            return render_template('contact_page/contact_good.html', name=form.name.data, email=form.email.data)
    return render_template('/contact_page/contact.html', form=form)


#Tech Route
@app.route('/workshop')
def workshop():   
    return render_template('workshop.html')




if __name__ == "__main__":
    app.run(debug=False)