from flask import Blueprint, request, redirect, request, url_for, flash, Response
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
        email = request.json.get('credentials').get('email', None)
        password = request.json.get('credentials').get('password', None)
    elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
        email= credentials(request.data)['credentials']['email']
        password= credentials(request.data)['credentials']['password']
    if not email:
        if request.content_type == 'application/json':
            return Response('Missing email!', mimetype='application/json', status=400)
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            return Response('Missing email!', mimetype='text/html', status=400)
    if not password:
        if request.content_type == 'application/json':
            return Response('Missing password!', mimetype='application/json', status=400)
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            return Response('Missing password!', mimetype='text/html', status=400)
    #check for same email
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
        if request.content_type == 'application/json':
            return Response('Login successfully!', mimetype='application/json')
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            return Response('Login successfully!', mimetype='text/html')
    else:
        if request.content_type == 'application/json':
            return Response('Login failed!', mimetype='application/json', status=400)
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            return Response('Login failed!', mimetype='text/html', status=400)

@auth_blueprint.route('/api/signup', methods=['POST'])
def signup_post():
    email = None
    password = None
    name = None
    if request.content_type == 'application/json':
        email = request.json.get('credentials').get('email', None)
        password = request.json.get('credentials').get('password', None)
        name = request.json.get('credentials').get('name', None)
    elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
        email= credentials(request.data)['credentials']['email']
        password= credentials(request.data)['credentials']['password']
        name= credentials(request.data)['credentials']['name']
    if not email:
        if request.content_type == 'application/json':
            return Response('Missing email!', mimetype='application/json', status=400)
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            return Response('Missing email!', mimetype='text/html', status=400)
    if not password:
        if request.content_type == 'application/json':
            return Response('Missing password!', mimetype='application/json', status=400)
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            return Response('Missing password!', mimetype='text/html', status=400)
    if not name:
        if request.content_type == 'application/json':
            return Response('Missing name!', mimetype='application/json', status=400)
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            return Response('Missing name!', mimetype='text/html', status=400)
    #check for same email
    user = User.query.filter_by(email=email).first()
    if user:
        if request.content_type == 'application/json':
            return Response('No account!', mimetype='application/json', status=400)
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            return Response('No account!', mimetype='text/html', status=400)
    #hash password
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(email=email, password=hashed, name=name)
    db.session.add(new_user)
    db.session.commit()
    if request.content_type == 'application/json':
        return Response('Signup successfully!', mimetype='application/json')
    elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
        return Response('Signup successfully!', mimetype='text/html')

#UPDATE user
@auth_blueprint.route('/api/resources/user', methods=['PUT'])
def user_put():
    request_id = request.args.get('id')
    
    if request_id is None:
        return 'No id', 400
    else:
        update = User.query.filter_by(id=request_id).first()
        email = None
        password = None
        name = None
        if request.content_type == 'application/json':
            email = request.json.get('credentials').get('email', None)
            password = request.json.get('credentials').get('password', None)
            name = request.json.get('credentials').get('name', None)
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            email= credentials(request.data)['credentials']['email']
            password= credentials(request.data)['credentials']['password']
            name= credentials(request.data)['credentials']['name']
        else:
            return Response('Wrong content type!',mimetype='application/json', status=400)
        if name is not None:
             update.name = name
        if email is not None:
            update.email = email
        if password is not None:
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            update.password = hashed
        db.session.commit()
        if request.content_type == 'application/json':
            return Response('User updated',mimetype='application/json')
        if request.content_type == 'application/xml' or request.content_type == 'text/xml':
            return Response('User updated',mimetype='text/xml')

#DELETE user
@auth_blueprint.route('/api/resources/user', methods=['DELETE'])
def user_delete():
    request_id = request.args.get('id')
    if request_id is None:
        return 'No id', 400
    else:
        if request.content_type == 'application/json':
            user = User.query.filter_by(id=request_id)
            if user is None:
                return Response('Wrong ID',mimetype='application/json', status=400)
            user.delete()
            db.session.commit()
            return Response('User deleted',mimetype='application/json')
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            user = User.query.filter_by(id=request_id)
            if user is None:
                return Response('Wrong ID',mimetype='text/xml', status=400)
            user.delete()
            db.session.commit()
            return Response('User deleted',mimetype='text/xml')
