from datetime import datetime

from flask import g, Blueprint, flash, redirect, url_for, render_template, request, jsonify, session

from flask_login import current_user, login_user, logout_user, login_required
from flask_jwt_extended import create_access_token

from werkzeug.utils import secure_filename

from my_app import login_manager, db, config
from my_app.config import ALLOWED_EXTENSIONS_FILES_AVATAR

from my_app.auth import operations
from my_app.auth.models import User
from my_app.auth.forms import ResgistrationForm, LoginForm, ChangeUserInformationForm, ChangeUserAddressForm, ChangeUserPasswordForm, UserSocialNetworkForm, AvatarForm, LangForm
from my_app.auth.helpers import authenticate
from my_app.documents import operations as doc_operations
from my_app.util.user.confirmation import confirm_token, generate_confirmation_token
from my_app.util.email.email import send_email

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

        token = generate_confirmation_token(user.email)
        # TODO send email
        html = render_template('user/email_confirm_user.html', token=token)
        send_email(user.email, 'Confirm account',html)

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

@authRoute.route('/confirm_email/<token>', methods=('GET',))
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The token is invalid', 'danger')
        return redirect(url_for('tasks.index'))

    #token is valid
    user = User.query.filter_by(email=email).first_or_404()
    user.email_confirmed_at = datetime.now()
    user = operations.update(user)
    session['user'] = user.serialize

    flash('User confirm', 'success')
    return redirect(url_for('tasks.index'))

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


#----profile
@authRoute.route('/user/profile')
@login_required
def profile():

    userdb = operations.getById(session['user']['id'])

    #basic info
    changeUserInformationForm = ChangeUserInformationForm()
    changeUserInformationForm.firstname.data = session['user']['first_name']
    changeUserInformationForm.lastname.data = session['user']['last_name']
    changeUserInformationForm.email.data = session['user']['email']

    # address
    changeUserAddressForm = ChangeUserAddressForm()
    if userdb.address_id is not None:
        changeUserAddressForm.address.data = userdb.address.address

    # password
    changeUserPasswordForm = ChangeUserPasswordForm()

    #social red
    socialNeworks = operations.getAllSocialNetwork()
    socialNeworkForm = UserSocialNetworkForm()
    socialNeworksUser = operations.getSocialNetworkByUserId(userId=userdb.id)

    #avatar
    avatarForm = AvatarForm()

    #lang
    langDefault = 'EN'
    if userdb.lang:
        langDefault = userdb.lang.value

    langForm = LangForm(lang=langDefault)
    # langForm.lang.default = #userdb.lang.value

    return render_template('user/profile.html',changeUserInformationForm=changeUserInformationForm, changeUserAddressForm=changeUserAddressForm, changeUserPasswordForm=changeUserPasswordForm, socialNeworks=socialNeworks, socialNeworkForm=socialNeworkForm,socialNeworksUser=socialNeworksUser, avatarForm=avatarForm, langForm=langForm)

@authRoute.route('/change-information', methods=('POST',))
@login_required
def changeInformation():
    
    form = ChangeUserInformationForm()

    if form.validate_on_submit():

        userAuth = operations.getById(session['user']['id'], True)
        userAuth.first_name = form.firstname.data
        userAuth.last_name = form.lastname.data
        userAuth.email = form.email.data

        session['user'] = userAuth.serialize

        operations.update(userAuth) 

    if form.errors:
        flash(form.errors, 'danger')
        
    return redirect(url_for('auth.profile'))

@authRoute.route('/change-address', methods=('POST',))
@login_required
def changeAddress():
    
    form = ChangeUserAddressForm()

    if form.validate_on_submit():

        userAuth = operations.getById(session['user']['id'], True)

        if userAuth.address_id is None:
            #create
            address = operations.createAddress(form.address.data)
            userAuth.address_id = address.id
            operations.update(userAuth)
        else:
            #update
            address = operations.updateAddress(userAuth.address_id, form.address.data)

    if form.errors:
        flash(form.errors, 'danger')
        
    return redirect(url_for('auth.profile'))

@authRoute.route('/change-password', methods=('POST',))
@login_required
def changePassword():
    
    form = ChangeUserPasswordForm()

    if form.validate_on_submit():

        userAuth = operations.getById(session['user']['id'], True)
        userAuth.hash_password(form.password.data)
        operations.update(userAuth)
        
    if form.errors:
        flash(form.errors, 'danger')
        
    return redirect(url_for('auth.profile'))

@authRoute.route('/save-social-network', methods=('POST',))
@login_required
def saveSocialNetwork():
    
    form = UserSocialNetworkForm()

    if form.validate_on_submit():
        userAuth = operations.getById(session['user']['id'], True)
        operations.saveSocialNetwork(userAuth.id, form.social_network_id.data, form.name.data)
    if form.errors:
        flash(form.errors, 'danger')
        
    return redirect(url_for('auth.profile'))


@authRoute.route('/delete-social-network', methods=('GET',))
@login_required
def deleteSocialNetwork():
    socialNetworkId = request.args.get('social_network_id', type=int)
    operations.deleteSocialNetwork(session['user']['id'], socialNetworkId)
    return redirect(url_for('auth.profile'))

@authRoute.route('/avatar/upload', methods=('POST',))
@login_required
def avatarUpload():
    
    form = AvatarForm()
    if form.validate_on_submit():
        f = form.avatar.data
        if f and config.allowed_extensions_file(f.filename,list=ALLOWED_EXTENSIONS_FILES_AVATAR):
            filename = secure_filename(f.filename)
            document = doc_operations.create(filename, filename.lower().rsplit('.',1)[1],'/avatar',f)
            
            # update user
            userAuth = operations.getById(session['user']['id'], True)
            userAuth.avatar_id = document.id
            operations.update(userAuth)

            session['user'] = userAuth.serialize

    return redirect(url_for('auth.profile'))

@authRoute.route('/avatar/destroy', methods=('POST',))
@login_required
def avatarDestroy():
    
    #search user
    userAuth = operations.getById(session['user']['id'], True)

    # avatar id to delete
    document_id = userAuth.avatar_id

    # delete avatar to user and document
    userAuth.avatar_id = None
    operations.update(userAuth)
    doc_operations.delete(document_id,'/avatar')

    # reset the sesion
    userAuth = operations.getById(session['user']['id'], True)
    session['user'] = userAuth.serialize

    return redirect(url_for('auth.profile'))

@authRoute.route('/lang', methods=('POST',))
@login_required
def lang():    
    form = LangForm()
    if form.validate_on_submit():
        userAuth = operations.getById(session['user']['id'], True)
        userAuth.lang = form.lang.data
        userAuth = operations.update(userAuth)
        session['user'] = userAuth.serialize
    if form.errors:
        flash(form.errors, 'danger')
        
    return redirect(url_for('auth.profile'))

#----profile