from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SubmitField

class AddForm(FlaskForm):
    name = StringField('Full Name: ')
    email = StringField('Email: ')
    facebook = StringField('Facebook: ')
    twitter =  StringField('Twitter: ')
    linkedin = StringField('Linkedin: ')
    github = StringField('Github: ')
    submit = SubmitField('sign up')
