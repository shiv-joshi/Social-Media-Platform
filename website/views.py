# contains all the routes in the website
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
from .models import *
import json

views = Blueprint('views', __name__)

# decorator defines the route for the function below to run
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        post = request.form.get("post")

        new_post = Post(data=post, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        flash('Post added!', category='success')

    users = User.query.all()
    users_mapping = {user.id: user for user in users}
    return render_template("home.html", user=current_user, users=users, users_mapping=users_mapping)

@views.route('/delete-post', methods=['POST'])
def delete_post():
    post = json.loads(request.data) # turn the JSON string into a python dict
    postId = post['postId'] # access the postId parameter
    post = Post.query.get(postId)
    if post:
        # if post belongs to person who is signed in
        if post.user_id == current_user.id:
            db.session.delete(post)
            db.session.commit()
        # dont let ppl delete other users posts
    
    return jsonify({})

@views.route('/edit-post', methods=['POST'])
def edit_post():
    post = json.loads(request.data)
    postId = post['postId']
    newText = post['newText']
    post = Post.query.get(postId)
    
    if post:
        post.data = newText
        db.session.commit()
    flash('Updated post!', category='success')
    return jsonify({})

@views.route('/add-comment', methods=['POST'])
def add_comment():
    comment = json.loads(request.data)
    postId = comment['postId']
    text = comment['commentText']
    
    new_comment = Comment(data=text, post_id=postId , user_id=current_user.id)
    db.session.add(new_comment)
    db.session.commit()

    return jsonify({})