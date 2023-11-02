"""File containing SQLAlchemy model classes"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc


# This is the connection to the database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()

##################################################################

# Model definitions

"""Models for Blogly."""

class User(db.Model):
    """class for SQLAlchemy model User"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text)

    def __repr__(self):
        e = self
        return f"<User {e.id} {e.first_name} {e.last_name}, {e.image_url}>"
    
    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"
    


####### Helper functions

def connect_db(app):
    """Connect the database to our Flask app."""

    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # So that we can use Flask-SQLAlchemy, we'll make a Flask app
    from app import app
    connect_db(app)

    db.drop_all()
    db.create_all()