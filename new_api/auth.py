from flask import Blueprint, request, redirect, request, url_for, flash
import bcrypt
from database import db
from models import User
from response_builder import credentials

auth_blueprint = Blueprint('auth_blueprint', __name__)

@auth_blueprint.route('/api/login', methods=['POST'])
def login_post():
    email = None
    password = None
    if request.content_type == 'application/json':
        email = request.json.get('email', None)
        password = request.json.get('password', None)
    elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
        email= credentials(request.data)['credentials']['email']
        password= credentials(request.data)['credentials']['password']
    if not email:
        return 'Missing email!', 400
    if not password:
        return 'Missing password!', 400
    #check for same email
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
        return 'Login successfully', 200
    else:
        return 'Login unsuccessfull', 400

@auth_blueprint.route('/api/login')
def login():
    return 'Login here!'

@auth_blueprint.route('/api/signup', methods=['POST'])
def signup_post():
    email = None
    password = None
    name = None
    if request.content_type == 'application/json':
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        name = request.json.get('name', None)
    elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
        email= credentials(request.data)['credentials']['email']
        password= credentials(request.data)['credentials']['password']
        name= credentials(request.data)['credentials']['name']
    if not email:
        return 'Missing email!', 400
    if not password:
        return 'Missing password!', 400
    if not name:
        return 'Missing name!', 400
    #check for same email
    user = User.query.filter_by(email=email).first()
    if user:
        return redirect(url_for('auth_blueprint.signup'))
    #hash password
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(email=email, password=hashed, name=name)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth_blueprint.login'))

@auth_blueprint.route('/api/signup')
def signup():
    return 'Signup here!'

@auth_blueprint.route('/api/logout')
def logout():
    return 'Logout'
