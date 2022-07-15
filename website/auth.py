import re
from flask import Blueprint, redirect, render_template, request, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from . import db

from .models import User

auth = Blueprint('auth', __name__)

# E-mail regex
emailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    return render_template('login.html', text='user')

@auth.route('/logout')
def logout():
    return render_template('logout.html')

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if not re.fullmatch(emailRegex, email):
            flash('Invalid E-mail', category='error')
        elif len(username) < 4:
            flash('Username must be longer than 3 characters', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 8:
            flash('Password must be longer than 8 characters.', category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit

            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('sign_up.html')