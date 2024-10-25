# Importing necessary modules from Flask and Flask-WTF
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField 
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError ,Optional
from VertechX.models import User  # Assuming 'User' model is imported from your app
from flask_login import current_user

# SignupForm class: Handles user registration with validation for username, email, and password confirmation
class SignupForm(FlaskForm):
    # Username field: A text field for the user's name with validation rules
    username = StringField(
        label='User Name : ',  # Label displayed next to the input field
        validators=[Length(min=2, max=30), DataRequired()]
    )
    # Validation Explanation:
    # - Length(min=2, max=30): Ensures the username is between 2 and 30 characters long
    # - DataRequired(): Ensures the field is not left empty
    
    # Email field: A text field for the user's email with validation to ensure a valid email format
    email = StringField(
        label='Email Address : ',  # Label displayed next to the input field
        validators=[Email(), DataRequired()]
    )
    # Validation Explanation:
    # - Email(): Ensures the entered email is in the correct email format (e.g., user@example.com)
    # - DataRequired(): Ensures the field is not left empty
    
    # Password field: First password input with validation to ensure it's at least 6 characters long
    password1 = PasswordField(
        label='Password : ',  # Label displayed next to the input field
        validators=[Length(min=6), DataRequired()]
    )
    # Validation Explanation:
    # - Length(min=6): Ensures the password is at least 6 characters long
    # - DataRequired(): Ensures the field is not left empty
    
    # Password confirmation field: Second password input to confirm password matches
    password2 = PasswordField(
        label='Confirm Password : ',  # Label displayed next to the input field
        validators=[EqualTo('password1'), DataRequired()]
    )
    # Validation Explanation:
    # - EqualTo('password1'): Ensures the second password matches the first one
    # - DataRequired(): Ensures the field is not left empty
    
    # Submit button: A button that submits the form when clicked
    submit = SubmitField('Submit')

    # Custom validation for the username: Checks if the entered username is unique
    def validate_username(self, username):
        # Check if a user with the entered username already exists in the database
        user = User.query.filter_by(Username=username.data).first()
        if user:
            # If the username already exists, raise a ValidationError with a custom message
            raise ValidationError('User Name is already Exist, Please Enter another one')

    # Custom validation for the email: Checks if the entered email is unique
    def validate_email(self, email):
        # Check if a user with the entered email already exists in the database
        existing_email = User.query.filter_by(Email_Address=email.data).first()
        if existing_email:
            # If the email already exists, raise a ValidationError with a custom message
            raise ValidationError('Email Address is already Exist, Please Enter another one')

# SigninForm class: Handles user login with validation for username and password
class SigninForm(FlaskForm):
    # Username field for the sign-in form: Requires a valid username
    username = StringField(
        label='User Name : ',  # Label displayed next to the input field
        validators=[DataRequired()]
    )
    # Validation Explanation:
    # - DataRequired(): Ensures the field is not left empty
    
    # Password field for the sign-in form: Requires a valid password
    password = PasswordField(
        label='Password : ',  # Label displayed next to the input field
        validators=[DataRequired()]
    )
    # Validation Explanation:
    # - DataRequired(): Ensures the field is not left empty
    
    # Submit button for the sign-in form: A button that submits the form when clicked
    submit = SubmitField(label='Sign in : ')


class ProfileForm(FlaskForm):
    username = StringField(
        label='User Name : ', 
        validators=[Length(min=2, max=30), DataRequired()]
    )
    email = StringField(
        label='Email Address : ', 
        validators=[Email(), DataRequired()]
    )
    password = PasswordField(
        label='New Password : ', 
        validators=[Length(min=6), Optional()]
    )
    submit = SubmitField('Save Changes')

    # Ensure unique username and email if they are changed
    def validate_username(self, username):
        if username.data != current_user.Username:
            user = User.query.filter_by(Username=username.data).first()
            if user:
                raise ValidationError('Username is already in use. Please choose another one.')

    def validate_email(self, email):
        if email.data != current_user.Email_Address:
            user = User.query.filter_by(Email_Address=email.data).first()
            if user:
                raise ValidationError('Email is already in use. Please choose another one.')
