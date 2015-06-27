from flask_wtf import Form
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.validators import DataRequired

class pageFill(Form):
    title = StringField('Page Title', validators=[DataRequired()])
    text = TextAreaField('Page Content', validators=[DataRequired()])
    style = TextAreaField('Custom Page Style')
    color = TextAreaField('Slide Background Color')

class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class siteConfig(Form):
    siteTitle = StringField('Site Title', validators=[DataRequired()])
