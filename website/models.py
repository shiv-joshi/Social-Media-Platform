# from current package
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# db.Model just means that all objects of this type need to look like this and have these attributes
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(100))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True) # generates automatically
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    comments = db.relationship('Comment') 
    # foreign key references a primary key in another table to reduce dupes
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # foreign key is lowercase

class User(db.Model, UserMixin):
    # define schema/tables
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    # find relationship to Post table
    posts = db.relationship('Post') # table is uppercase
