import os
import gunicorn
import psycopg2
from flask import Flask, render_template, url_for, request, redirect
from flask_mail import Mail, Message
from forms.contact_form import ContactForm

app = Flask(__name__)

app.config["SECRET_KEY"] = "os.getenv('SECRET_KEY')"
app.config["MAIL_SERVER"] = os.getenv('MAIL_SERVER')
app.config["MAIL_USERNAME"] = os.getenv('MAIL_USERNAME')
app.config["MAIL_PASSWORD"] = os.getenv('MAIL_PASSWORD')
app.config["MAIL_PORT"] = os.getenv('MAIL_PORT')
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

horse_list = [
        {
            "id":0,
            "name": "Ty",
            "age": "16",
            "breed":"American Mustang",
            "bio": "Ty is a little shy but is very willing to please. He has no trouble giving up his feet and loading on a trailer. He has been saddled and I have been on his back. We are still working on walking off.",
            "pic":"https://upload.wikimedia.org/wikipedia/commons/d/d6/Smile_Of_A_Horse_%28139382329%29.jpeg", 
            "sex":"Gelding", 
            "color":"Red Dun",
            "training": "Picks up all four feet, and allows picking. Takes the saddle and has taken a rider. No problem loading."
        },
         {
            "id":1,
            "name": "Jet",
            "age": "16",
            "breed":"American Mustang",
            "bio": "Ty is a little shy but is very willing to please. He has no trouble giving up his feet and loading on a trailer. He has been saddled and I have been on his back. We are still working on walking off.",
            "pic":"https://cdn.pixabay.com/photo/2020/07/02/21/25/horse-5364441_1280.jpg", 
            "sex":"Mare", 
            "color":"Black",
            "training": "Picks up all four feet, and allows picking. Takes the saddle and has taken a rider. No problem loading."
        },
         {
            "id":2,
            "name": "Sundance",
            "age": "16",
            "breed":"American Mustang",
            "bio": "Ty is a little shy but is very willing to please. He has no trouble giving up his feet and loading on a trailer. He has been saddled and I have been on his back. We are still working on walking off.",
            "pic":"https://static1.bigstockphoto.com/2/6/3/large1500/362810416.jpg", 
            "sex":"Gelding", 
            "color":"Bay",
            "training": "Picks up all four feet, and allows picking. Takes the saddle and has taken a rider. No problem loading."
        },
         {
            "id":3,
            "name": "Sue",
            "age": "16",
            "breed":"American Mustang",
            "bio": "Ty is a little shy but is very willing to please. He has no trouble giving up his feet and loading on a trailer. He has been saddled and I have been on his back. We are still working on walking off.",
            "pic":"https://cdn.pixabay.com/photo/2016/09/01/19/54/horse-1637400_1280.jpg", 
            "sex":"Mare", 
            "color":"Gray",
            "training": "Picks up all four feet, and allows picking. Takes the saddle and has taken a rider. No problem loading."
        },
         {
            "id":4,
            "name": "Ty",
            "age": "16",
            "breed":"American Mustang",
            "bio": "Ty is a little shy but is very willing to please. He has no trouble giving up his feet and loading on a trailer. He has been saddled and I have been on his back. We are still working on walking off.",
            "pic":"https://upload.wikimedia.org/wikipedia/commons/d/d6/Smile_Of_A_Horse_%28139382329%29.jpeg", 
            "sex":"Gelding", 
            "color":"Red Dun",
            "training": "Picks up all four feet, and allows picking. Takes the saddle and has taken a rider. No problem loading."
        }         
    ]

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


@app.route("/horses")
def horses():
    global horse_list
    return render_template('horses.html', horses= horse_list)

@app.route("/horses/<id>/<name>")
def horse(name, id):
    for horse in horse_list:        
        if horse["id"] == int(id):
            selected_horse = horse
            return render_template('horse.html', horse=selected_horse)
    return redirect(url_for('horses'))
        

if __name__ == "__main__":
    app.run(debug=True)
