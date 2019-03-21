from wtforms import validators, Form, TextField, IntegerField
from wtforms.validators import DataRequired, Email, Length
from .model import User, Chat

class UserForm(Form):
    first_name = TextField ('first_name', validators=[DataRequired(), Length(max=40)])
    last_name = TextField ('last_name', validators=[DataRequired(), Length(max=40)])
    nick = TextField('nick', validators=[DataRequired(), Length(max=30)])
    email = TextField('email', validators=[Email()])

class ChatForm(Form):
    first_id = IntegerField('first_id', validators=[DataRequired()])
    second_id = IntegerField('second_id', validators=[DataRequired()])