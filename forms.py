from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField, PasswordField, IntegerField
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from domdit.models import User


class AdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create New Admin')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class Login(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class Email(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('test')


class PortfolioForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    languages = StringField('Languages:', validators=[DataRequired()])
    short_description = StringField('Short Description:', validators=[DataRequired()])
    description = TextAreaField('Description:')
    url = StringField('Full url:', validators=[DataRequired()])
    git = StringField('git URL:', validators=[DataRequired()])
    folder = StringField('Image Folder Name:', validators=[DataRequired()])
    thumb = FileField('Thumbnail:', validators=[FileAllowed(['jpg', 'png', 'gif'])])
    img1 = FileField('Image 1:', validators=[FileAllowed(['jpg', 'png', 'gif'])])
    img2 = FileField('Image 2:', validators=[FileAllowed(['jpg', 'png', 'gif'])])
    img3 = FileField('Image 3:', validators=[FileAllowed(['jpg', 'png', 'gif'])])
    submit = SubmitField('Submit')


class TestimonialForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    site_name = StringField('Site Name:', validators=[DataRequired()])
    url = StringField('URL:', validators=[DataRequired()])
    text = TextAreaField('Testimonial:')
    img = FileField('Image:', validators=[FileAllowed(['jpg', 'png', 'gif'])])
    portfolio_id = IntegerField('Portfolio ID #:', validators=[DataRequired()])
    folder = StringField('Image Folder Name:', validators=[DataRequired()])
    submit = SubmitField('Submit')




