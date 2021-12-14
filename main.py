import os

import gunicorn
import psycopg2
from flask import Flask, render_template, url_for, request, redirect
from flask_mail import Mail, Message

from forms.contact_form import ContactForm

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')
app.config["MAIL_SERVER"] = os.getenv('MAIL_SERVER')
app.config["MAIL_USERNAME"] = os.getenv('MAIL_USERNAME')
app.config["MAIL_PASSWORD"] = os.getenv('MAIL_PASSWORD')
app.config["MAIL_PORT"] = os.getenv('MAIL_PORT')
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template('index.html')


@app.route("/contact_me", methods=['GET', 'POST'])
def contact_me():
    form = ContactForm()
    if form.validate_on_submit():
        msg = Message("Please Help Message", sender="tim@tccs.tech", recipients=["tim@tccs.tech"])
        msg.body = request.form["message"]
        mail.send(msg)
        return render_template('contact_page/contact_good.html', name=form.name.data, email=form.email.data)
    return render_template('/contact_page/contact.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
