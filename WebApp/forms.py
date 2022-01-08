from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class Form(FlaskForm):
    sayi = StringField('Sayi')
    buton = SubmitField('Oku')
