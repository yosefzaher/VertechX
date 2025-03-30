# Import necessary modules from Flask and related packages
from flask import render_template, redirect, url_for, flash ,request ,jsonify
from VertechX import app, db  # Import the app and db objects from your project
from VertechX.models import User  # Import the User model
from VertechX.forms import SignupForm, SigninForm  # Import form classes for signup and signin
from flask_login import login_user, logout_user, login_required  # For user authentication and session management
from flask_login import current_user  # To access the currently logged-in user
from VertechX.forms import ProfileForm  # Add the ProfileForm we’ll create shortly
from VertechX.automatic import AutoMode


# List of page endpoints to navigate between
pages = [
    'Home_Page',        # Home page endpoint
    'About_Page',       # About page endpoint
    'VM_Page',          # VM page endpoint
    'Features_Page',    # Features page endpoint
    'Integration_Page' # Integration page endpoint
]

#To Store the current Mode (manual or automatic)
current_mode = "manual"

#Create an instance of AutoMode
auto_mode = AutoMode() 

# Route for the Home page
@app.route('/')
def Home_Page():
    """
    Render the home page of the website.

    This route is responsible for displaying the main landing page of the website.

    Parameters:
    - None

    Behavior:
    - When accessed, the home page is rendered with the `Home.html` template.

    Flash Messages:
    - None

    Returns:
    - A rendered HTML page displaying the home content, served from `Home.html`.

    Example Usage:
    - Navigating to the root URL `/` will display the home page.

    Security Considerations:
    - Ensure the home page content is not sensitive or should not be restricted.
    """
    return render_template('Home.html')




# Route for the About page
@app.route('/about')
def About_Page():
    """
    Render the about page of the website.

    This route displays information about the website, such as its purpose, team, or history.

    Parameters:
    - None

    Behavior:
    - When accessed, the about page is rendered with the `About.html` template.

    Flash Messages:
    - None

    Returns:
    - A rendered HTML page displaying the about content, served from `About.html`.

    Example Usage:
    - Navigating to `/about` will display the about page.

    Security Considerations:
    - Ensure no sensitive or confidential information is disclosed on this page.
    """
    return render_template('About.html')




# Route for the VM page
@app.route('/vm')
def VM_Page():
    """
    Render the VM (Virtual Machine) page.

    This route is responsible for displaying information related to the virtual machine setup or configuration.

    Parameters:
    - None

    Behavior:
    - When accessed, the VM page is rendered with the `VM.html` template.

    Flash Messages:
    - None

    Returns:
    - A rendered HTML page displaying the VM content, served from `VM.html`.

    Example Usage:
    - Navigating to `/vm` will display the virtual machine-related page.

    Security Considerations:
    - Ensure that any virtual machine-related configurations or sensitive data is properly protected.
    """
    return render_template('VM.html')




# Route for the Features page
@app.route('/features')
def Features_Page():
    """
    Render the features page.

    This route displays the various features available on the website or product.

    Parameters:
    - None

    Behavior:
    - When accessed, the features page is rendered with the `Features.html` template.

    Flash Messages:
    - None

    Returns:
    - A rendered HTML page displaying the features of the website, served from `Features.html`.

    Example Usage:
    - Navigating to `/features` will display the features page.

    Security Considerations:
    - Ensure that no private or confidential features are exposed unnecessarily.
    """
    return render_template('Features.html')




# Route for the Integration page
@app.route('/integration')
def Integration_Page():
    """
    Render the integration page.

    This route displays information related to the integration of the system with other tools or services.

    Parameters:
    - None

    Behavior:
    - When accessed, the integration page is rendered with the `Integration.html` template.

    Flash Messages:
    - None

    Returns:
    - A rendered HTML page displaying integration-related content, served from `Integration.html`.

    Example Usage:
    - Navigating to `/integration` will display the integration page.

    Security Considerations:
    - Ensure integration-related data and services are not exposed without appropriate authentication or authorization.
    """
    return render_template('Integration.html')



@app.route('/previous/<current_page>')
def previous_page(current_page):
    """
    Navigate to the previous page in the 'pages' list based on the current page.

    This route allows navigation through a list of pages. Given the name of the current page,
    it determines the previous page in the sequence and redirects to it. If the current page is the 
    first one in the list, the function will loop back to the last page.

    Parameters:
    - current_page: The name of the current page, passed in the URL. This helps to determine
      the previous page in the sequence.

    Behavior:
    - If the current page is found in the 'pages' list:
        - The index of the current page is located.
        - The index of the previous page is calculated by decrementing the current index by 1.
        - The previous page is determined using modulo to handle the case where the first page should
          loop back to the last page.
    - If the current page is not found in the list, a 404 error is returned with a 'Page not found' message.

    Flash Messages:
    - None

    Redirect:
    - Redirects to the previous page in the sequence, or loops back to the last page if the current page
      is the first in the list.

    Returns:
    - A redirect to the URL of the previous page.
    - If the current page is not found, returns a 404 error.

    Example Usage:
    - A user navigates to `/previous/page2`, and the app redirects them to the previous page in the sequence.
    - If the current page is the first page in the list, e.g., `page1` in a list of `['page1', 'page2', 'page3']`,
      the user will be redirected to `page3`.

    Security Considerations:
    - Ensure that the list of pages (`pages`) is trusted, as it is used to determine valid page names
      and routing behavior. Make sure no unexpected pages are included.

    """
    try:
        # Find the index of the current page in the pages list
        current_index = pages.index(current_page)
    except ValueError:
        # If the page is not found in the list, return a 404 error
        return "Page not found", 404

    # Calculate the index of the previous page, using modulo to wrap around to the last page if needed
    previous_index = (current_index - 1) % len(pages)

    # Redirect to the previous page
    return redirect(url_for(pages[previous_index]))




@app.route('/next/<current_page>')
def next_page(current_page):
    """
    Navigate to the next page in the 'pages' list based on the current page.

    This route allows navigation through a list of pages. Given the name of the current page,
    it determines the next page in the sequence and redirects to it. If the current page is the 
    last one in the list, the function will loop back to the first page.
    # You can add GPIO handling logic here if needed:
    # Example:
    # GPIO.output(mode_pin, GPIO.HIGH if mode == "automatic" else GPIO.LOW)
    Parameters:
    - current_page: The name of the current page, passed in the URL. This helps to determine
      the next page in the sequence.

    Behavior:
    - If the current page is found in the 'pages' list:
        - The index of the current page is located.
        - The index of the next page is calculated by incrementing the current index by 1.
        - The next page is determined using modulo to handle the case where the last page should
          loop back to the first page.
    - If the current page is not found in the list, a 404 error is returned with a 'Page not found' message.

    Flash Messages:
    - None

    Redirect:
    - Redirects to the next page in the sequence, or loops back to the first page if the current page
      is the last in the list.

    Returns:
    - A redirect to the URL of the next page.
    - If the current page is not found, returns a 404 error.

    Example Usage:
    - A user navigates to `/next/page2`, and the app redirects them to the next page in the sequence.
    - If the current page is the last page in the list, e.g., `page3` in a list of `['page1', 'page2', 'page3']`, 
      the user will be redirected to `page1`.

    Security Considerations:
    - Ensure that the list of pages (`pages`) is trusted, as it is used to determine valid page names
      and routing behavior. Make sure no unexpected pages are included.

    """
    try:
        # Find the index of the current page in the pages list
        current_index = pages.index(current_page)
    except ValueError:
        # If the page is not found in the list, return a 404 error
        return "Page not found", 404

    # Calculate the index of the next page, using modulo to wrap around to the first page if needed
    next_index = (current_index + 1) % len(pages)

    # Redirect to the next page
    return redirect(url_for(pages[next_index]))




@app.route('/Signup', methods=['POST', 'GET'])
def Signup_Page():
    """
    This route handles user registration, including form validation and saving the user to the database.

    Methods:
    - GET: Renders the signup page with the registration form.
    - POST: Processes the form submission, validates the input, and creates a new user account.

    Parameters:
    - form: A SignupForm object that captures the user's registration details (username, email, password).

    Behavior:
    - When a GET request is made, the signup form is displayed.
    - When a POST request is made and the form is valid:
        - A new user object is created with the data provided by the user.
        - The new user is saved to the database.
        - The user is logged in automatically after account creation.
        - A success message is flashed.
        - The user is redirected to the home page.
    - If the form has errors (e.g., invalid email or password mismatch), appropriate error messages are flashed to the user.

    Flash Messages:
    - A success message is displayed when the account is created and the user is logged in.
    - Errors are flashed for invalid fields (such as invalid email or mismatched passwords).

    Redirect:
    - Redirects the user to the home page after successful signup.

    Returns:
    - If the form is valid and the user is created, the user is redirected to the home page.
    - If the form has errors, the signup page is rendered again with error messages.

    Example Usage:
    - A user visits the `/Signup` route to create a new account, entering their details in the form.
    - Upon form submission, if the credentials are valid, a new account is created, the user is logged in, and they are redirected to the home page.
    - If the form is invalid, error messages are displayed and the user is prompted to correct the issues.

    Security Considerations:
    - Ensure the password is securely hashed before being stored in the database (assumes `Password` field is hashed).
    - The user's session is immediately created after account creation, ensuring they are logged in.

    """
    # Initialize the signup form
    form = SignupForm()

    # If the form is submitted and validated
    if form.validate_on_submit():
        # Create a new user object with the provided data
        user_to_create = User(
            Username=form.username.data,
            Password=form.password1.data,  # Assuming password is hashed before saving
            Email_Address=form.email.data
        )

        # Add the user to the database and commit the changes
        db.session.add(user_to_create)
        db.session.commit()

        # Log the user in after account creation
        login_user(user_to_create)

        # Flash a success message and redirect to the home page
        flash(f'Account created successfully! Now You are Logged in as {user_to_create.Username}', 'success')
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




@app.route('/Signin', methods=['POST', 'GET'])
def Signin_Page():
    """
    This route handles user login functionality.

    Methods:
    - GET: Renders the signin page with the login form.
    - POST: Processes the form submission, validating the username and password.

    Parameters:
    - form: A SigninForm object containing the user's credentials (username and password).

    Behavior:
    - When a GET request is made, the signin form is displayed.
    - When a POST request is made with valid credentials:
      - The user is authenticated by checking the username and password.
      - If the credentials are valid, the user is logged in, and a success message is flashed.
      - If the credentials are invalid, an error message is flashed.
    
    Access Control:
    - The user is redirected to the home page after successful login.

    Flash Messages:
    - Displays a success message with the username if the login is successful.
    - Displays an error message if the login fails due to incorrect username or password.

    Redirect:
    - Redirects the user to the 'Home_Page' route upon successful login.
    
    Security Considerations:
    - The form validation ensures that the username and password are checked properly before logging the user in.

    Returns:
    - If the form is valid, a redirect response to the home page.
    - If the form is invalid, the signin page is rendered again with error messages.

    Example Usage:
    - A user visits the `/Signin` route and submits their login credentials using the Signin form.

    Notes:
    - The password is checked against the stored password hash using the `Check_Password` method.
    - After a successful login, the user’s session is created, and they are considered authenticated.

    """
    # Initialize the signin form
    form = SigninForm()

    # If the form is submitted and validated
    if form.validate_on_submit():
        # Attempt to find the user by their username
        attempted_user = User.query.filter_by(Username=form.username.data).first()

        # Check if the user exists and the provided password is correct
        if attempted_user and attempted_user.Check_Password(Attempted_Password=form.password.data):
            # Log in the user
            login_user(attempted_user)

            # Flash a success message and redirect to the home page
            flash(f'Success, You Logged in as: {attempted_user.Username}', category='success')
            return redirect(url_for('Home_Page'))
        else:
            # If credentials are invalid, flash an error message
            flash('Username and password do not match, please try again', category='danger')

    # Render the signin page with the form
    return render_template('Signin.html', form=form)




@app.route('/logout')
@login_required
def Logout_Page():
    """
    This route handles the user logout process.

    Methods:
    - GET: Logs the user out of the application and redirects them to the home page.

    Access Control:
    - @login_required: Ensures that only authenticated users can access this route.

    Behavior:
    - Logs the user out of the application using the `logout_user()` function.
    - Displays a flash message to inform the user that they have successfully logged out.
    - Redirects the user to the home page after logout.

    Flash Messages:
    - Displays an informational message indicating the user has been logged out.

    Redirect:
    - Redirects the user to the 'Home_Page' route after logging out.

    Example Usage:
    - A GET request to `/logout` triggers the logout process and redirects the user to the home page.

    Security Considerations:
    - The `@login_required` decorator ensures that the route cannot be accessed unless the user is logged in.

    Returns:
    - Redirect response to the home page after logout.

    Notes:
    - After logging out, the user's session is cleared, and they will need to log in again to access protected routes.
    """
    # Log out the current user
    logout_user()

    # Notify the user that they have been logged out
    flash('You Have been Logged Out!', category='info')

    # Redirect to the home page
    return redirect(url_for('Home_Page'))



@app.route("/dashboard", methods=['GET'])
@login_required
def Dashboard_Page():
    """
    This route renders the dashboard page and sets the greenhouse mode based on the query string.

    Method:
    - GET: This route accepts only GET requests.

    Access Control:
    - @login_required: Ensures that only authenticated users can access this page.

    Query Parameters:
    - mode (str): The operational mode of the greenhouse.
        - "automatic": Enables automatic control of the greenhouse.
        - "manual": Enables manual control of the greenhouse.
        - Defaults to "automatic" if no mode is specified.

    Behavior:
    - Depending on the mode, this route updates the GPIO pin state to reflect the greenhouse's current mode:
        - "automatic": Sets the GPIO pin `mode_pin` to HIGH (LED ON).
        - "manual": Sets the GPIO pin `mode_pin` to LOW (LED OFF).

    Returns:
    - Renders the 'Dashboard.html' template with the current mode as a context variable.

    Template Variables:
    - mode (str): The current mode passed to the template for rendering.

    Example Usage:
    - /dashboard?mode=automatic
    - /dashboard?mode=manual
    """

    return render_template('Dashboard.html', mode=current_mode)




@app.route("/api/mode", methods=['POST'])
@login_required  # If you want this route to be protected
def change_mode():
    """
    API endpoint to change the greenhouse mode.

    Method:
    - POST: Accepts a JSON payload to update the mode.

    Request Payload:
    - { "mode": "automatic" }  or  { "mode": "manual" }

    Behavior:
    - Updates the system mode based on the received JSON data.

    Returns:
    - JSON response with success message and the updated mode.
    """
    global current_mode 

    data = request.get_json()
    if not data or "mode" not in data:
        return jsonify({"error": "Missing 'mode' parameter"}), 400

    mode = data["mode"]
    
    if mode not in ["automatic", "manual"]:
        return jsonify({"error": "Invalid mode"}), 400


    if mode == "automatic" :
        auto_mode.start()
    elif mode == "manual" :
        auto_mode.stop()

    current_mode = mode 
    print(f"The Mode Changed To {current_mode}.")
    
    return jsonify({"message": f"Mode changed to {mode}", "mode": mode})


@app.route("/api/get_mode", methods=['GET'])
@login_required
def get_mode():
    """
    API endpoint for FastAPI to retrieve the current greenhouse mode.
    """
    return jsonify({"mode": current_mode})




@app.route('/profile', methods=['GET', 'POST'])
@login_required
def Profile_Page():
    """
    This route handles the user's profile page, allowing them to view and update their profile details.

    Methods:
    - GET: Renders the profile page with the user's current information pre-filled in the form.
    - POST: Processes updates to the user's profile details, including username, email, and password.

    Access Control:
    - @login_required: Ensures that only authenticated users can access this page.

    Behavior:
    - On GET request:
        - Pre-populates the form with the current user's data (username and email).
    - On POST request:
        - Validates the form input.
        - Updates the user's username, email, and password (if a new password is provided).
        - Commits the changes to the database.
        - Redirects back to the profile page with a success message.

    Form Handling:
    - `ProfileForm` is used to handle user input validation.
    - `form.validate_on_submit()`: Ensures that the submitted data passes all validation checks.

    Flash Messages:
    - Displays a success message to the user upon successfully updating their profile.

    Template Variables:
    - form: The `ProfileForm` object is passed to the template for rendering and validation.

    Returns:
    - Renders the 'Profile.html' template with the form object.

    Example Usage:
    - Access the profile page: `/profile` (GET request).
    - Update profile details: Submit the form on `/profile` (POST request).
    """

    # Create an instance of the profile form
    form = ProfileForm()

    if form.validate_on_submit():
        # Update the current user's username and email address with the form data
        current_user.Username = form.username.data
        current_user.Email_Address = form.email.data

        # Update the user's password only if a new password is provided in the form
        if form.password.data:
            current_user.set_password(form.password.data)

        # Save the updated user information to the database
        db.session.commit()

        # Notify the user of a successful profile update
        flash('Your profile has been updated.', 'success')

        # Redirect to the profile page to display updated information
        return redirect(url_for('Profile_Page'))

    # Pre-populate the form with the user's existing data during a GET request
    elif request.method == 'GET':
        form.username.data = current_user.Username
        form.email.data = current_user.Email_Address

    # Render the profile template with the populated or updated form
    return render_template('Profile.html', form=form)



@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    """
    This route handles the deletion of a user's account.

    Methods:
    - POST: Deletes the authenticated user's account from the database.

    Access Control:
    - @login_required: Ensures that only authenticated users can access this route.

    Behavior:
    - Deletes the user's account from the database.
    - Logs the user out of the application.
    - Displays an informational flash message indicating successful account deletion.
    - Redirects the user to the home page.

    Important Notes:
    - This action is irreversible and permanently removes the user's account and all associated data.
    - The route uses the POST method to ensure that account deletion is not accidentally triggered by a simple page visit or link.

    Security Considerations:
    - Ensure the form that triggers this route uses CSRF protection to prevent unauthorized deletion.
    - Only authenticated users can access this route due to the `@login_required` decorator.

    Flash Messages:
    - Displays an informational message to the user upon account deletion.

    Redirect:
    - Redirects the user to the 'Home_Page' route after the account is deleted.

    Returns:
    - Redirect response to the home page.

    Example Usage:
    - A POST request to `/delete_account` is triggered from a form or button, resulting in account deletion.
    """

    # Retrieve the current user
    user = current_user

    # Delete the user from the database
    db.session.delete(user)
    db.session.commit()

    # Log the user out of the application
    logout_user()

    # Notify the user of successful account deletion
    flash('Your account has been deleted.', 'info')

    # Redirect to the home page
    return redirect(url_for('Home_Page'))






