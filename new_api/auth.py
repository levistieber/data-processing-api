from flask import Blueprint, request, redirect, request, url_for, flash, Response, make_response, jsonify
import bcrypt
from database import db
from models import User
from response_builder import credentials, get_user, get_user_xml, get_users, get_users_xml, signup_request, error_toxml
import validator
from errors import errors_dic, custom_errors_dic

auth_blueprint = Blueprint('auth_blueprint', __name__)

@auth_blueprint.route('/api/login', methods=['POST'])
def login_post():
    email = None
    password = None
    if request.content_type == 'application/json':
        if validator.validateJsonResponse(r'validators\json\login_schema.json', request.json):
            return make_response(jsonify(custom_errors_dic[0]), 400)
        email = request.json.get('credentials').get('email', None)
        password = request.json.get('credentials').get('password', None)
    elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
        if validator.validateXmlResponse(r'validators\xml\login_schema.xsd', request.data) is False:
            return Response(error_toxml(custom_errors_dic[0]), mimetype='text/xml', status=400)
        email= credentials(request.data)['credentials']['email']
        password= credentials(request.data)['credentials']['password']
    if not email:
        if request.content_type == 'application/json':
            return make_response(jsonify(errors_dic[7]), 422)
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            return Response(error_toxml(errors_dic[7]), mimetype='text/xml', status=422)
    if not password:
        if request.content_type == 'application/json':
            return make_response(jsonify(errors_dic[7]), 422)
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            return Response(error_toxml(errors_dic[7]), mimetype='text/xml', status=422)
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
        if request.content_type == 'application/json':
            return Response('Login successfully!', mimetype='application/json')
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            return Response('Login successfully!', mimetype='text/xml')
    else:
        if request.content_type == 'application/json':
            return make_response(jsonify(errors_dic[0]), 400)
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            return Response(error_toxml(errors_dic[0]), mimetype='text/xml', status=400)

#CREATE USER
@auth_blueprint.route('/api/signup', methods=['POST'])
def signup_post():
    email = None
    password = None
    name = None
    if request.content_type == 'application/json':
        if validator.validateJsonResponse(r'validators\json\signup_put_user_schema.json', request.json):
            return make_response(jsonify(custom_errors_dic[0]), 400)
        name = list(request.json.get('user'))[0]
        email = request.json.get('user').get(name).get('credentials').get('email', None)
        password = request.json.get('user').get(name).get('credentials').get('password', None)
    elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
        if validator.validateXmlResponse(r'validators\xml\signup_schema.xsd', request.data) is False:
            return Response(error_toxml(custom_errors_dic[0]), mimetype='text/xml', status=400)
        name= list(signup_request(request.data)['user'])[0]
        email= signup_request(request.data)['user'][name]['credentials']['email']
        password= signup_request(request.data)['user'][name]['credentials']['password']
    if not email:
        if request.content_type == 'application/json':
            return make_response(jsonify(errors_dic[7]), 422)
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            return Response(error_toxml(errors_dic[7]), mimetype='text/xml', status=422)
    if not password:
        if request.content_type == 'application/json':
            return make_response(jsonify(errors_dic[7]), 422)
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            return Response(error_toxml(errors_dic[7]), mimetype='text/xml', status=422)
    if not name:
        if request.content_type == 'application/json':
            return make_response(jsonify(errors_dic[7]), 422)
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            return Response(error_toxml(errors_dic[7]), mimetype='text/xml', status=422)
    #check for same email
    user = User.query.filter_by(email=email).first()
    if user:
        if request.content_type == 'application/json':
            return make_response(jsonify(errors_dic[4]), 409)
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            return Response(error_toxml(errors_dic[4]), mimetype='text/xml', status=409)
    #hash password
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(email=email, password=hashed, name=name)
    db.session.add(new_user)
    db.session.commit()
    if request.content_type == 'application/json':
        return Response('Signup successfully!', mimetype='application/json')
    elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
        return Response('Signup successfully!', mimetype='text/xml')

#GET user
@auth_blueprint.route('/api/resources/user')
def user():
    request_id = request.args.get('id')
    
    if request_id is None:
        if request.content_type == 'application/json':
            result = User.query.all()
            if validator.validateJsonResponse(r'validators\json\get_user_schema.json', get_users(result)):
                return make_response(jsonify(custom_errors_dic[0]), 400)
            return make_response(jsonify(get_users(result)), 200)
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            result = User.query.all()
            if validator.validateXmlResponse(r'validators\xml\get_user_schema.xsd', get_users_xml(result)) is False:
                return Response(error_toxml(custom_errors_dic[0]), mimetype='text/xml', status=400)
            return Response(get_users_xml(result), mimetype='text/xml',status=200)
    else:
        if request.content_type == 'application/json':
            result = User.query.filter_by(id=request_id).first()
            if validator.validateJsonResponse(r'validators\json\get_user_schema.json', get_user(result)):
                return make_response(jsonify(custom_errors_dic[0]), 400)
            return make_response(jsonify(get_user(result)), 200)
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            result = User.query.filter_by(id=request_id).first()
            if validator.validateXmlResponse(r'validators\xml\get_user_schema.xsd', get_user_xml(result)) is False:
                return Response(error_toxml(custom_errors_dic[0]), mimetype='text/xml', status=400)
            return Response(get_user_xml(result), mimetype='text/xml',status=200)

#UPDATE user
@auth_blueprint.route('/api/resources/user', methods=['PUT'])
def user_put():
    request_id = request.args.get('id')
    
    if request_id is None:
        if request.content_type == 'application/json':
            return make_response(jsonify(errors_dic[0]), 400)
        else:
            return Response(error_toxml(errors_dic[0]), mimetype='text/xml', status=400)
    else:
        update = User.query.filter_by(id=request_id).first()
        email = None
        password = None
        name = None
        if request.content_type == 'application/json':
            if validator.validateJsonResponse(r'validators\json\signup_put_user_schema.json', request.json):
                return make_response(jsonify(custom_errors_dic[0]), 400)
            name = list(request.json.get('user'))[0]
            email = request.json.get('user').get(name).get('credentials').get('email', None)
            password = request.json.get('user').get(name).get('credentials').get('password', None)
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            if validator.validateXmlResponse(r'validators\xml\signup_schema.xsd', request.data) is False:
                return Response(error_toxml(custom_errors_dic[0]), mimetype='text/xml', status=400)
            name= list(signup_request(request.data)['user'])[0]
            email= signup_request(request.data)['user'][name]['credentials']['email']
            password= signup_request(request.data)['user'][name]['credentials']['password']
        else:
            return make_response(jsonify(errors_dic[6]), 415)
        if update is None:
            if request.content_type == 'application/json':
                return make_response(jsonify(errors_dic[2]), 404)
            if request.content_type == 'application/xml' or request.content_type == 'text/xml':
                return Response(error_toxml(errors_dic[2]), mimetype='text/xml', status=404)
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
        if request.content_type == 'application/json':
            return make_response(jsonify(errors_dic[0]), 400)
        else:
            return Response(error_toxml(errors_dic[0]), mimetype='text/xml', status=400)
    else:
        if request.content_type == 'application/json':
            user = User.query.filter_by(id=request_id)
            if user is None:
                return make_response(jsonify(errors_dic[2]), 404)
            user.delete()
            db.session.commit()
            return Response('User deleted',mimetype='application/json')
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            user = User.query.filter_by(id=request_id)
            if user is None:
                return Response(error_toxml(errors_dic[2]), mimetype='text/xml', status=404)
            user.delete()
            db.session.commit()
            return Response('User deleted',mimetype='text/xml')
