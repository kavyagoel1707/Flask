from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app as app
from werkzeug.security \
         import generate_password_hash, check_password_hash
from models import User
from flask_login import login_user, logout_user, \
                                     login_required, current_user
from __init__ import db
auth=Blueprint('auth',__name__)
@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    else: #if the method is post then we check if the user exists with the right password
        email=request.form.get('email')
        password=request.form.get('password')
        remember= True if request.form.get('remember') else False
        user=User.query.filter_by(email=email).first()
        #checking if user exits
        if not user: 
            flash('Please sign up before!')
            return redirect(url_for('auth.signup'))
        #checking if password is correct using hashed password
        elif not check_password_hash(user.password,password):
            flash('Incorrect Password')
            return redirect(url_for('auth.login'))
        #if check passes, that means user has entered right credentials, he is logged in
        login_user(user,remember=remember)
        return redirect(url_for('main.profile'))

@auth.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='GET':
        return render_template('signup.html')
    else: #if method is post
        email=request.form.get('email')
        name=request.form.get('name')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        #checking if user already exists or not, if it does redirect to signup page
        if user: 
            flash('Email already exists!')
            return redirect(url_for('auth.signup'))
        #creating new user with the inputeed dteails and hashing the password
        new_user=User(email=email,name=name,password=generate_password_hash(password,method='sha256'))
        #adding user details to the database
        db.session.add(new_user)
        db.session.commit()
        #logged in, redirecting to profile page
        return redirect(url_for('main.profile'))

@auth.route('/logout')
def logout():
    logout_user() #logout function
    return redirect(url_for('main.index'))