from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,EmailField,DateField,SubmitField,IntegerField
from wtforms.validators import DataRequired,Email,Length

class LoginForm(FlaskForm):
    email= EmailField("Email",validators=[DataRequired()])
    password= PasswordField("Password",validators=[DataRequired()])
    submit=SubmitField('Submit')

class RegisterForm(FlaskForm):
    username= StringField("Username",validators=[DataRequired()])
    email= EmailField("Email",validators=[DataRequired()])
    password= PasswordField("Password",validators=[DataRequired(),Length(max=8)])
    confirm_password= PasswordField("Confirm Password",validators=[DataRequired(),Length(max=8)])
    submit=SubmitField('Submit')

class EventForm(FlaskForm):
    title=StringField("Title",validators=[DataRequired()])
    description=StringField('Description')
    date=DateField('Date',validators=[DataRequired()])
    location=StringField('Location',validators=[DataRequired()])
    capacity=IntegerField('Capacity',validators=[DataRequired()])
    phone=StringField('Phone',validators=[DataRequired()])
    submit=SubmitField('Create Event')
