import gunicorn
import psycopg2
from flask import Flask, render_template, url_for

from forms.contact_form import ContactForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "af3asd356f4as3d1fs5d"


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template('index.html')


@app.route("/contact_me", methods=["GET", "POST"])
def contact_me():
    form = ContactForm()
    return render_template('contact.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
