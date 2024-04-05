from website import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)




class User(db.Model, UserMixin):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(128))

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
       return check_password_hash(self.password_hash, password)


class Reservering(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bungalow_id = db.Column(db.Integer, db.ForeignKey('bungalow.id'), nullable=False)
    week = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Bungalowpark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    naam = db.Column(db.String(100), nullable=False)
    locatie = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    image_url = db.Column(db.String(200), nullable=True)
    bungalows = db.relationship('Bungalow', backref='bungalowpark', lazy=True)

    def __repr__(self):
        return f"Bungalowpark('{self.naam}', '{self.locatie}')"




