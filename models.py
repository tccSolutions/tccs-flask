from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Horse(db.Model):
    __tablename__ ="horses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    breed = db.Column(db.String, nullable=False)
    sex = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    training = db.Column(db.String, nullable=False)
    saddle_time = db.Column(db.String, nullable=False)
    bio = db.Column(db.String, nullable=False)

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
            "bio": self.bio
        }
