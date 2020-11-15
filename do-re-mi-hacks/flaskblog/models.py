from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):     # used in order to manage sessions
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):   # creates a User database model
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    specialization = db.Column(db.String(30), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    musician_available = db.Column(db.Boolean, nullable=False)
    timings = db.Column(db.String(50), nullable=False)
    # defines the one to many relationship of a user to his/her posts
    # the author attribute is used to get the details of the user who created the post, from a post itself
    # the lazy argument means that SQLAlchemy will load all the data (posts) of a user in one go
    Event = db.relationship('Event', backref='author', lazy=True)

    # how the object is printed
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role}')"


class Event(db.Model):   # creates a Post database model
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Event('{self.title}', '{self.date_posted}')"
