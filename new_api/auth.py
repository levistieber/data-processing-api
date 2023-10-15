from flask import Blueprint, request, redirect, request, url_for, flash, Response, make_response, jsonify
import bcrypt
from database import db
from models import User
from response_builder import credentials, get_user, get_user_xml, get_users, get_users_xml, signup_request, error_toxml
import validator
from errors import errors_dic, custom_errors_dic

auth_blueprint = Blueprint('auth_blueprint', __name__)

#API route for Login
@auth_blueprint.route('/api/login', methods=['POST'])
def login_post():
    email, password = None, None

    #Save content type of request in a variable
    content_type = request.content_type

    #Saving possible content types in variables
    contents_xml = ('application/xml', 'text/xml')
    content_json = 'application/json'

    #Check if request is in JSON
    if content_type == content_json:
        #Validate request against Json schema
        if validator.validateJsonResponse(r'validators\json\login_schema.json', request.json):
            return make_response(jsonify(custom_errors_dic[0]), 400)
        #Extract email and password from request
        email = request.json.get('credentials').get('email', None)
        password = request.json.get('credentials').get('password', None)

    #Check if request is in XML
    elif content_type in contents_xml:
        #Validate request against XML schema
        if validator.validateXmlResponse(r'validators\xml\login_schema.xsd', request.data) is False:
            return Response(error_toxml(custom_errors_dic[0]), mimetype='text/xml', status=400)
        #Extract email and password from request
        email= credentials(request.data)['credentials']['email']
        password= credentials(request.data)['credentials']['password']

    #Check if email and password are in request, or missing. If missing any of them missing, return error 422
    if not email or not password:
        if content_type == content_json:
            return make_response(jsonify(errors_dic[7]), 422)
        elif content_type in contents_xml:
            return Response(error_toxml(errors_dic[7]), mimetype='text/xml', status=422)

    #Database query to find user with the email in the request
    user = User.query.filter_by(email=email).first()

    #Check if credentials are correct
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
        #Successful login response
        if content_type == content_json:
            return Response('Login successful!', mimetype='application/json')
        elif content_type in contents_xml:
            return Response('Login successful!', mimetype='text/xml')
    else:
        #Failed login response (error)
        if content_type == content_json:
            return make_response(jsonify(errors_dic[0]), 400)
        elif content_type in contents_xml:
            return Response(error_toxml(errors_dic[0]), mimetype='text/xml', status=400)

#API route for creating a user
@auth_blueprint.route('/api/signup', methods=['POST'])
def signup_post():
    email, password, name = None, None, None

    #Save content type of request in a variable
    content_type = request.content_type
    
    #Saving possible content types in variables
    contents_xml = ('application/xml', 'text/xml')
    content_json = 'application/json'

    #Check if request is in JSON
    if content_type == content_json:
        #Validate request against Json schema
        if validator.validateJsonResponse(r'validators\json\signup_put_user_schema.json', request.json):
            return make_response(jsonify(custom_errors_dic[0]), 400)
        #Extract email, password and name from request
        name = list(request.json.get('user'))[0]
        email = request.json.get('user').get(name).get('credentials').get('email', None)
        password = request.json.get('user').get(name).get('credentials').get('password', None)

    #Check if request is in XML
    elif content_type in contents_xml:
        #Validate request against Json schema
        if validator.validateXmlResponse(r'validators\xml\signup_schema.xsd', request.data) is False:
            return Response(error_toxml(custom_errors_dic[0]), mimetype='text/xml', status=400)
        #Extract email, password and name from request
        name= list(signup_request(request.data)['user'])[0]
        email= signup_request(request.data)['user'][name]['credentials']['email']
        password= signup_request(request.data)['user'][name]['credentials']['password']

    #Check if email, password and name are in request, or missing. If any of them missing, return error 422
    if not email or not password or not name:
        if content_type == content_json:
            return make_response(jsonify(errors_dic[7]), 422)
        elif content_type in contents_xml:
            return Response(error_toxml(errors_dic[7]), mimetype='text/xml', status=422)
        
    #Database query to find user with the email in the request
    user = User.query.filter_by(email=email).first()

    #Check if this user already exists. If yes, return error message
    if user:
        if content_type == content_json:
            return make_response(jsonify(errors_dic[4]), 409)
        elif content_type in contents_xml:
            return Response(error_toxml(errors_dic[4]), mimetype='text/xml', status=409)
        
    #Hash password
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    #Create new user with given credentials and add them to database
    new_user = User(email=email, password=hashed, name=name)
    db.session.add(new_user)
    db.session.commit()

    #Successful signup response
    if content_type == content_json:
        return Response('Signup successful!', mimetype='application/json')
    elif content_type contents_xml:
        return Response('Signup successful!', mimetype='text/xml')

#API endpoint for retrieving user
@auth_blueprint.route('/api/resources/user')
def user():
    #Get the id parameter from the request
    request_id = request.args.get('id')

    #Save content type of request in a variable
    content_type = request.content_type

    #Saving possible content types in variables
    contents_xml = ('application/xml', 'text/xml')
    content_json = 'application/json'

    #Check if id is present or not in the request
    if request_id is None:
    #No id in request
        if content_type == content_json:
            #Retrieve all user records from database and validate the JSON response
            result = User.query.all()
            if validator.validateJsonResponse(r'validators\json\get_user_schema.json', get_users(result)) is False:
                return make_response(jsonify(custom_errors_dic[0]), 400)
            return make_response(jsonify(get_users(result)), 200)
        
        elif content_type in contents_xml:
            #Retrieve all user records from database and validate the XML response
            result = User.query.all()
            if validator.validateXmlResponse(r'validators\xml\get_user_schema.xsd', get_users_xml(result)) is False:
                return Response(error_toxml(custom_errors_dic[0]), mimetype='text/xml', status=400)
            return Response(get_users_xml(result), mimetype='text/xml',status=200)

    else:
    #Id is in the request
        if content_type == content_json:
            #Retrieve user from database with id in request, and validate the JSON response
            result = User.query.filter_by(id=request_id).first()
            if validator.validateJsonResponse(r'validators\json\get_user_schema.json', get_user(result)) is False:
                return make_response(jsonify(custom_errors_dic[0]), 400)
            return make_response(jsonify(get_user(result)), 200)
        elif content_type in contents_xml:
            #Retrieve user from database with id in request, and validate the XML response
            result = User.query.filter_by(id=request_id).first()
            if validator.validateXmlResponse(r'validators\xml\get_user_schema.xsd', get_user_xml(result)) is False:
                return Response(error_toxml(custom_errors_dic[0]), mimetype='text/xml', status=400)
            return Response(get_user_xml(result), mimetype='text/xml',status=200)

#API endpoint for updating user
@auth_blueprint.route('/api/resources/user', methods=['PUT'])
def user_put():
    #Get the id parameter from the request
    request_id = request.args.get('id')

    #Save content type of request in a variable
    content_type = request.content_type

    #Saving possible content types in variables
    contents_xml = ('application/xml', 'text/xml')
    content_json = 'application/json'

    #Check if id is present in the request. If not, error response
    if request_id is None:
        if content_type == content_json:
            return make_response(jsonify(errors_dic[0]), 400)
        elif content_type in contents_xml:
            return Response(error_toxml(errors_dic[0]), mimetype='text/xml', status=400)
    #Id is in request
    else:
        #Retrieve the user to be updated based on the provided 'id'
        update = User.query.filter_by(id=request_id).first()
        email, password, name = None, None, None

        if content_type == content_json:
            #Validate response with JSON schema
            if validator.validateJsonResponse(r'validators\json\signup_put_user_schema.json', request.json):
                return make_response(jsonify(custom_errors_dic[0]), 400)
            #Extract relevant data from the JSON request
            name = list(request.json.get('user'))[0]
            email = request.json.get('user').get(name).get('credentials').get('email', None)
            password = request.json.get('user').get(name).get('credentials').get('password', None)

        elif content_type in contents_xml:
            #Validate response with XML schema
            if validator.validateXmlResponse(r'validators\xml\signup_schema.xsd', request.data) is False:
                return Response(error_toxml(custom_errors_dic[0]), mimetype='text/xml', status=400)
            #Extract relevant data from the XML request
            name= list(signup_request(request.data)['user'])[0]
            email= signup_request(request.data)['user'][name]['credentials']['email']
            password= signup_request(request.data)['user'][name]['credentials']['password']
        else:
            #Error response if request is not in json or xml
            return make_response(jsonify(errors_dic[6]), 415)

        #Check if user to be updated exists. If not, error response 404
        if update is None:
            if content_type == content_json:
                return make_response(jsonify(errors_dic[2]), 404)
            if content_type in contents_xml:
                return Response(error_toxml(errors_dic[2]), mimetype='text/xml', status=404)

        #Update information that is provided
        if name is not None:
            update.name = name
        if email is not None:
            update.email = email
        if password is not None:
            #Hash password
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            update.password = hashed

        #Commit changes to database
        db.session.commit()

        #Return success response for user update
        if content_type == content_json:
            return Response('User updated successfully!',mimetype='application/json')
        if content_type in contents_xml:
            return Response('User updated successfully!',mimetype='text/xml')

#DELETE user
@auth_blueprint.route('/api/resources/user', methods=['DELETE'])
def user_delete():
    #Get the id parameter from the request
    request_id = request.args.get('id')

    #Save content type of request in a variable
    content_type = request.content_type

    #Saving possible content types in variables
    contents_xml = ('application/xml', 'text/xml')
    content_json = 'application/json'

    #Check if id in request is present. If not, error response 400
    if request_id is None:
        if content_type == content_json:
            return make_response(jsonify(errors_dic[0]), 400)
        elif content_type in contents_xml:
            return Response(error_toxml(errors_dic[0]), mimetype='text/xml', status=400)
    #If id is present
    else:
        #Query the user to be deleted based on the provided 'id'
        user = User.query.filter_by(id=request_id)
        
        if content_type == content_json:
            #If user does not exist, reutnr error 404
            if user is None:
                return make_response(jsonify(errors_dic[2]), 404)
            #Delete the user and commit the changes to the database
            user.delete()
            db.session.commit()
            #Return success response
            return Response('User deleted successfully!',mimetype='application/json')
        
        elif content_type in contents_xml:
            #If user does not exist, reutnr error 404
            if user is None:
                return Response(error_toxml(errors_dic[2]), mimetype='text/xml', status=404)
            #Delete the user and commit the changes to the database
            user.delete()
            db.session.commit()
            #Return success response
            return Response('User deleted successfully!',mimetype='text/xml')
