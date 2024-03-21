from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange
from wtforms import ValidationError, IntegerField
from website.models import User

class BungalowparkForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    rating = IntegerField('Rating', validators=[NumberRange(min=0, max=5)])
    submit = SubmitField('Submit')

class ReservationForm(FlaskForm):
    bungalow = StringField('Bungalow', validators=[DataRequired()])
    type = StringField('Type')
    grootte = StringField('Grootte')
    week = StringField('Week', validators=[DataRequired()])
    username = StringField('Gebruikersnaam', validators=[DataRequired()])
    password = PasswordField('Wachtwoord', validators=[DataRequired()])
    submit = SubmitField('Reserveer')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Leg vast!')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Dit e-mailadres staat al geregistreerd!')
        return True

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Deze gebruikersnaam is al vergeven, probeer een ander naam!')
        return True

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Inloggen')



