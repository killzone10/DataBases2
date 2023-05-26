from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField,FileAllowed
from pyparsing import countedArray
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TelField,IntegerField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from app.models import User,Invoice,Order



class RegistrationForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(),Length(min = 2,max = 20)])
    email = StringField('Email',
                            validators=[DataRequired(),Email()])
    password = PasswordField('Hasło',
                            validators=[DataRequired()])
    confirm_password = PasswordField('Potwierdź hasło',
                                validators=[DataRequired(),EqualTo('password')])
    
    submit = SubmitField('Zarejestruj się')


    def validate_username(self,username):

        user = User.query.filter_by(username = username.data).first()
        if user: #will be None if not in database
            raise ValidationError('Username already exist - choose different username')

    def validate_email(self,email):

        user = User.query.filter_by(email = email.data).first()
        if user: #will be None if not in database
            raise ValidationError('Email already exist - choose different email')

class LoginForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(),Length(min = 2,max = 20)])
    password = PasswordField('Password',
                            validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Zaloguj się')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(),Length(min = 2,max = 20)])
    email = StringField('Email',
                            validators=[DataRequired(),Email()])
   
    first_name = StringField('Imie',
                            validators=[DataRequired(),Length(min = 2, max = 20)])

    second_name = StringField('Nazwisko',
                            validators=[DataRequired(),Length(min = 2, max = 20)])

    phone = TelField('Numer telefonu',validators=[DataRequired(),Length(min = 2, max = 10)])
   
   
    submit = SubmitField('Aktualizuj')


    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user: #will be None if not in database
                raise ValidationError('Username already exist - choose different username')

    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user: #will be None if not in database
                raise ValidationError('Email already exist - choose different email')

    # def validate_first_name(self,first_name):
    #     if first_name.data != current_user.first_name:
    #         user = User.query.filter_by(first_name = first_name.data).first()
    #         if user: #will be None if not in database
    #             raise ValidationError('Email already exist - choose different email')

class OrderForm(FlaskForm):

    email = StringField('Email',
                            validators=[DataRequired(),Email()])
   
    first_name = StringField('Imie',
                            validators=[DataRequired(),Length(min = 2, max = 20)])

    second_name = StringField('Nazwisko',
                            validators=[DataRequired(),Length(min = 2, max = 20)])

    phone = TelField('Numer telefonu',validators=[DataRequired(),Length(min = 2, max = 10)])


    country = StringField('Kraj',
                            validators=[DataRequired(),Length(min = 2,max = 40)])

    city = StringField('Miasto',
                            validators=[DataRequired(),Length(min = 2,max = 40)])


    street = StringField('Ulica',
                            validators=[DataRequired(),Length(min = 2,max = 40)])

    number = TelField('Numer mieszkania',validators=[DataRequired(),Length(min = 2, max = 10)])

    postal_code = StringField('Kod pocztowy',validators=[DataRequired(),Length(min = 2, max = 10)])
   
    invoice = BooleanField('Czy potrzebujesz faktury?')

    nip = TelField("NIP",validators=[Length(max = 10)])
    
    submit = SubmitField('Kup')
