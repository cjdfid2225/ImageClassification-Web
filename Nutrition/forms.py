from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo

class RegisterForm(FlaskForm):
    userid = StringField('userid', validators=[DataRequired()])
    userheight = StringField('userheight', validators=[DataRequired()])
    userweight = StringField('userweight', validators=[DataRequired()])
    userold = StringField('userold', validators=[DataRequired()])
    usersex = StringField('usersex', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), EqualTo('re_password')]) #equalTo("필드네임")
    re_password = PasswordField('re_password', validators=[DataRequired()])