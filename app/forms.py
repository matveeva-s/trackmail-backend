from wtforms import validators, Form, TextField, IntegerField, widgets, SelectField
from wtforms.validators import DataRequired, Email, Length
from .model import User, Chat

class UserForm(Form):
    first_name = TextField ('first_name', validators=[DataRequired(), Length(max=40)])
    last_name = TextField ('last_name', validators=[DataRequired(), Length(max=40)])
    nick = TextField('nick', validators=[DataRequired(), Length(max=30)])
    email = TextField('email', validators=[Email()])

class GroupChatForm(Form):
    topic = TextField('topic', validators=[DataRequired(), Length(max=50)])
    users = widgets.CheckboxInput()

class PersonalChatForm(Form):
    user = TextField('user', validators=[DataRequired(), Length(max=81)])

class UserSearchForm(Form):
    first_name = TextField('first_name', validators=[Length(max=40)])
    last_name = TextField('last_name', validators=[Length(max=40)])
