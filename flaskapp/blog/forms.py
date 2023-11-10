from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired


class NewBlogPostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    body = TextAreaField("Body", validators=[DataRequired()])
