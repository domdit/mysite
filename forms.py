from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField, PasswordField, IntegerField
from flask_wtf.file import FileAllowed
from flask_wtf import RecaptchaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from domdit.models import User, Tag


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


class TagField(StringField):

    def _value(self):
        if self.data:
            # Display tags as a comma separated list
            return ', '.join([tag.name for tag in self.data])
        return ''

    def get_tags_from_string(self, tag_string):
        raw_tags = tag_string.split(',')

        # filter empty tag names
        tag_names = [name.strip() for name in raw_tags if name.strip()]

        # query for already existing tags
        existing_tags = Tag.query.filter(Tag.name.in_(tag_names))

        # separate out the new names
        new_names = set(tag_names) - set([tag.name for tag in existing_tags])

        # create a list of unsaved tags
        new_tags = [Tag(name=name) for name in new_names]

        # return all the existing tags and all unsaved tags
        return list(existing_tags) + new_tags

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = self.get_tags_from_string(valuelist[0])
        else:
            self.data = []

class Login(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class Email(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    recaptcha = RecaptchaField(validators=[DataRequired()])
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


class NewBlogPost(FlaskForm):
    post_name = StringField('Name:', validators=[DataRequired()])
    content = TextAreaField('Blog Content:')
    thumb = FileField('Thumbnail:', validators=[FileAllowed(['jpg', 'png', 'gif'])])
    category = StringField('Category:', validators=[DataRequired()])
    tags = TagField('Tags:', description='Separate tags with commas')
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    text = TextAreaField('Comment:')
    email = StringField('Email')
    recaptcha = RecaptchaField(validators=[DataRequired()])
    comment_submit = SubmitField('Submit')

class Search(FlaskForm):
    term = StringField('Name:', validators=[DataRequired()])
    search_submit = SubmitField('Submit')