from flask import g, Blueprint, flash, redirect, url_for, render_template, request, jsonify, session

from flask_login import current_user, login_user, logout_user, login_required
from flask_jwt_extended import create_access_token

from my_app import login_manager, db

from my_app.auth.models import User
from my_app.auth.forms import ResgistrationForm, LoginForm
from my_app.auth.helpers import authenticate

authRoute = Blueprint('auth',__name__,)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@authRoute.before_request
def get_current_user():
    g.user = current_user



@authRoute.route('/register', methods=('GET', 'POST'))
def register():
    if current_user.is_authenticated:
        flash('Your are already logged in.', 'info')
        return redirect(url_for('tasks.index'))
    
    form = ResgistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash('This username has been already taken. Try another one', 'warning')
            return render_template('user/register.html', form=form)
        
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        flash('You are now registered. Please login.', 'success')

        if form.errors:
            flash(form.errors, 'danger')
        
    return render_template('user/register.html', form=form)

@authRoute.route('/login', methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        flash('Your are already logged in.', 'info')
        return redirect(url_for('tasks.index'))
    
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        existing_user = User.query.filter_by(username=username).first()
        if not(existing_user and existing_user.check_password(password)):
            flash('Invalid username or password', 'warning')
            return render_template('user/login.html', form=form)

        login_user(existing_user)
        session['user'] = existing_user.serialize
        flash('You have successfully logged in.', 'success')
        return redirect(url_for('tasks.index'))

    if form.errors:
        flash(form.errors, 'danger')
        
    return render_template('user/login.html', form=form)

@authRoute.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# JWT
@authRoute.route('/user/api', methods=['POST'])
def api():
    if not request.is_json:
        return jsonify({ "msj": "Missing JSN in request" }), 400
    
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username:
        return jsonify({"msj": "username not exit"}),400
    if not password:
        return jsonify({"msj": "password not exit"}),400
    
    user = authenticate(username,password)

    if not user:
        return jsonify({ "msj": "username or password not is correct" })
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200