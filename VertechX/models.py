from VertechX import db ,bcrypt ,login
from flask_login import UserMixin 

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model , UserMixin):
    """
    User class to represent a user in the database.
    
    Attributes:
    Id (int): The unique identifier for each user.
    Username (str): The user's unique username, cannot be null.
    Email_Address (str): The user's unique email address, cannot be null.
    Password_Hash (str): The hashed password of the user, cannot be null.
    """

    id = db.Column(db.Integer(), primary_key=True)
    Username = db.Column(db.String(length=30), nullable=False, unique=True)
    Email_Address = db.Column(db.String(length=50), nullable=False, unique=True)
    Password_Hash = db.Column(db.String(length=60), nullable=False, unique=False)

    def __repr__(self) -> str:
        """
        Returns a string representation of the User object.

        Returns:
        str: A string displaying the Username of the user.
        """
        return f"Username {self.Username}"
    
    @property
    def Password(self):
        """
        Property to get the Password attribute (not intended to be accessed directly).

        Returns:
        str: The current password of the user (hashed).
        """
        return self.Password

    @Password.setter
    def Password(self, Plain_Text_Password):
        """
        Setter method to hash the plain text password and store it in the Password_Hash attribute.

        Keyword arguments:
        Plain_Text_Password -- The plain text password provided by the user.
        
        Returns:
        None
        """
        self.Password_Hash = bcrypt.generate_password_hash(Plain_Text_Password).decode("utf-8")

    def Check_Password(self, Attempted_Password):
        """
        Checks if the attempted password matches the stored password hash.

        Keyword arguments:
        Attempted_Password -- The password that the user is trying to authenticate.
        
        Returns:
        bool: True if the attempted password matches the hashed password, False otherwise.
        """
        return bcrypt.check_password_hash(self.Password_Hash, Attempted_Password)


