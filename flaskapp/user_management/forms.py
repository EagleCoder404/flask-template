from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import  DataRequired


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


class LoginForm(FlaskForm):
    email = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

