# Import necessary modules from Flask and related packages
from flask import render_template, redirect, url_for, flash ,request
from VertechX import app, db  # Import the app and db objects from your project
from VertechX.models import User  # Import the User model
from VertechX.forms import SignupForm, SigninForm  # Import form classes for signup and signin
from flask_login import login_user, logout_user, login_required  # For user authentication and session management
from flask_login import current_user  # To access the currently logged-in user
from VertechX.forms import ProfileForm  # Add the ProfileForm we’ll create shortly


# List of page endpoints to navigate between
pages = [
    'Home_Page',        # Home page endpoint
    'About_Page',       # About page endpoint
    'VM_Page',          # VM page endpoint
    'Features_Page',    # Features page endpoint
    'Integration_Page' # Integration page endpoint
]


# Route for the Home page
@app.route('/')
def Home_Page():
    """Render the home page."""
    return render_template('Home.html')

# Route for the About page
@app.route('/about')
def About_Page():
    """Render the about page."""
    return render_template('About.html')

# Route for the VM page
@app.route('/vm')
def VM_Page():
    """Render the VM page."""
    return render_template('VM.html')

# Route for the Features page
@app.route('/features')
def Features_Page():
    """Render the features page."""
    return render_template('Features.html')

# Route for the Integration page
@app.route('/integration')
def Integration_Page():
    """Render the integration page."""
    return render_template('Integration.html')

# Route to navigate to the previous page in the list
@app.route('/previous/<current_page>')
def previous_page(current_page):
    """
    Navigate to the previous page in the 'pages' list based on the current page.
    If the current page is the first in the list, it loops back to the last page.
    """
    try:
        # Find the index of the current page
        current_index = pages.index(current_page)
    except ValueError:
        return "Page not found", 404  # If the page is not found in the list, return a 404 error

    # Calculate the index of the previous page
    previous_index = (current_index - 1) % len(pages)

    # Redirect to the previous page
    return redirect(url_for(pages[previous_index]))

# Route to navigate to the next page in the list
@app.route('/next/<current_page>')
def next_page(current_page):
    """
    Navigate to the next page in the 'pages' list based on the current page.
    If the current page is the last in the list, it loops back to the first page.
    """
    try:
        # Find the index of the current page
        current_index = pages.index(current_page)
    except ValueError:
        return "Page not found", 404  # If the page is not found in the list, return a 404 error

    # Calculate the index of the next page
    next_index = (current_index + 1) % len(pages)

    # Redirect to the next page
    return redirect(url_for(pages[next_index]))

# Route for the Signup page, allowing users to create a new account
@app.route('/Signup', methods=['POST', 'GET'])
def Signup_Page():
    """
    Handle user registration, including form validation and database saving.
    - If form is submitted and valid, a new user is created and logged in.
    - If form validation fails, appropriate error messages are flashed to the user.
    """
    form = SignupForm()  # Initialize the signup form
    if form.validate_on_submit():  # If the form is submitted and valid
        # Create a new user object
        user_to_create = User(
            Username=form.username.data,
            Password=form.password1.data,
            Email_Address=form.email.data
        )
        # Add the user to the database and commit
        db.session.add(user_to_create)
        db.session.commit()

        # Log the user in after account creation
        login_user(user_to_create)
        flash(f'Account created successfully! ,Now You are Logged in as {user_to_create.Username}', 'success')

        # Redirect to the home page after successful signup
        return redirect(url_for('Home_Page'))

    # If the form has errors, display them using flash messages
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                if 'email' in field:
                    flash('Invalid email address', 'danger')  # Flash error for invalid email
                elif 'password1' in field or 'password2' in field:
                    flash('Passwords do not match', 'warning')  # Flash warning for password mismatch
                else:
                    flash(error, 'danger')  # General flash for other errors

    # Render the signup template with the form
    return render_template('Signup.html', form=form)

# Route for the Signin page, allowing users to log in
@app.route('/Signin', methods=['POST', 'GET'])
def Signin_Page():
    """
    Handle user login, including form validation.
    - If credentials are valid, the user is logged in.
    - If invalid, a flash message informs the user to try again.
    """
    form = SigninForm()  # Initialize the signin form
    if form.validate_on_submit():  # If the form is submitted and valid
        # Try to find the user by username
        attempted_user = User.query.filter_by(Username=form.username.data).first()

        # Check if the user exists and the password matches
        if attempted_user and attempted_user.Check_Password(Attempted_Password=form.password.data):
            # Log in the user if credentials are valid
            login_user(attempted_user)
            flash(f'Success, You Logged in as: {attempted_user.Username}', category='success')
            return redirect(url_for('Home_Page'))
        else:
            # Flash a message if credentials are invalid
            flash('Username and password do not match, please try again', category='danger')

    # Render the signin template with the form
    return render_template('Signin.html', form=form)

# Route for logging out a user
@app.route('/logout')
@login_required
def Logout_Page():
    """
    Log the user out and redirect them to the home page.
    Flash a message to inform the user they have been logged out.
    """
    logout_user()  # Log out the current user
    flash('You Have been Logged Out!', category='info')  # Flash a message
    return redirect(url_for('Home_Page'))  # Redirect to the home page

@app.route("/dashboard", methods=['GET'])
@login_required
def Dashboard_Page():
    # Get the mode from the query string (defaults to 'automatic')
    mode = request.args.get('mode', 'automatic')
    return render_template('Dashboard.html', mode=mode)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def Profile_Page():
    form = ProfileForm()

    if form.validate_on_submit():
        # Update username and email
        current_user.Username = form.username.data
        current_user.Email_Address = form.email.data

        # Update password only if a new one is provided
        if form.password.data:
            current_user.set_password(form.password.data)

        # Commit the changes to the database
        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('Profile_Page'))

    # Pre-populate the form with existing user data on GET request
    elif request.method == 'GET':
        form.username.data = current_user.Username
        form.email.data = current_user.Email_Address

    return render_template('Profile.html', form=form)


@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user = current_user

    # Delete the user from the database
    db.session.delete(user)
    db.session.commit()

    # Log the user out
    logout_user()
    flash('Your account has been deleted.', 'info')
    return redirect(url_for('Home_Page'))








