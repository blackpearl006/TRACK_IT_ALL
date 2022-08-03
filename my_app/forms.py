from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateTimeLocalField, widgets,IntegerField,DateTimeField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, InputRequired
from my_app.models import User
#from wtforms.fields.html5 import DateTimeLocalField


widget = widgets.DateTimeInput()

class RegisterForm(FlaskForm):
    def validate_username(self,username_to_check):
        user=User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists !!')
    
    def validate_email(self,email_to_check):
        e_mail=User.query.filter_by(email=email_to_check.data).first()
        if e_mail:
            raise ValidationError('Email already Exists!! Try Logging in !!')

    username=StringField(label='Username: ', validators=[Length(min=2,max=30),DataRequired()])
    email=StringField(label='Email: ', validators=[Email(),DataRequired()])
    password1= PasswordField(label='Password: ', validators=[Length(min=6),DataRequired()])
    password2= PasswordField(label='Confirm Password: ', validators=[EqualTo('password1'),DataRequired()])
    submit=SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    username=StringField(label='User Name :', validators=[DataRequired()])
    password=PasswordField(label='Password', validators=[DataRequired()])
    submit=SubmitField(label='Sign In')

class UpdateFormTracker(FlaskForm):
    name=StringField(label='Name: ', validators=[Length(min=2,max=30),DataRequired()])
    description=StringField(label='Description: ', validators=[Length(min=2,max=30),DataRequired()])
    submit=SubmitField(label='Update')

class DeleteFormTracker(FlaskForm):
    submit=SubmitField(label='Delete')

class AddTracker(FlaskForm):
    name=StringField(label='Tracker Name: ', validators=[Length(min=2,max=30),DataRequired()])
    description=StringField(label='Description: ', validators=[Length(min=2,max=30),DataRequired()])
    type=SelectField(label='Tracker type',choices=[(1,'Numeric'),(2,'Muliple Choice'),(3,'Boolean'),(4,'Fahrenheit'),(5,'Calories'),(6,'Time')],validators=[InputRequired()])
    choices=StringField(label='choices: ')   
    submit=SubmitField(label='Add Tracker')
    # owner is the logged in person

class UpdateLog(FlaskForm):
    value=IntegerField(label='Value ', validators=[DataRequired()])
    note=StringField(label='note: ')
    submit=SubmitField(label='Update Log')

class DeleteLog(FlaskForm):
    submit=SubmitField(label='Delete Log')

class AddLog(FlaskForm):
    value=IntegerField(label='Value ', validators=[DataRequired()])
    timestamp=DateTimeLocalField(label='Time : ',format='%Y-%m-%dT%H:%M')    #something is wrong here
    note=StringField(label='note: ')
    desc=StringField(label='Description: ')
    submit=SubmitField(label='Add Log')

class UpdateProfile(FlaskForm):
    username=StringField(label='User Name :', validators=[DataRequired("Enter username")])
    email=StringField(label='Email: ', validators=[Email(),DataRequired()])
    city=StringField(label='City :')
    phone_num=IntegerField(label='Phone num ')
    target=IntegerField(label='Target ')
    social=StringField(label='Social media :')
    submit=SubmitField(label='Update Profile')
    
class AddChoices(FlaskForm):
    choices=StringField(label="choices : ")
    submit=SubmitField(label='Submit')