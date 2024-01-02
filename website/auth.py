from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db # means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

# if you refresh/load page its a GET and if you send data its a POST
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # if you are not j loading the page
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # look for all users who have this email
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Wrong password!', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        else:
            # create user
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
            password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            # redirect to homepage
            return redirect(url_for('views.home')) # can also do ('/)

    return render_template("sign_up.html", user=current_user) 

@auth.route('/my-posts')
@login_required
def my_posts():
    users = User.query.all()
    users_mapping = {user.id: user for user in users}
    return render_template("my_posts.html", user=current_user, users=users, users_mapping=users_mapping)


@auth.route('/logout')  
@login_required # makes sure that user is logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))