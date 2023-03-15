from xml.dom.minidom import parseString
from xml.etree.ElementTree import Element,tostring
from flask import Response
from flask import request, jsonify
from toxml import *
from errors import *

from api_mysql import mysql

from flask import Blueprint

api_users = Blueprint('api_users', __name__)

#USER APIS
@api_users.route('/application/login', methods=['POST'])
def log_in():
    requested_username = request.form['username']
    requested_password = request.form['password']
    requested_format = request.args.get('format')

    cursor = mysql.connection.cursor()
    cursor.execute(" SELECT id, username, password FROM user WHERE username =%s", (requested_username,))
    rv = cursor.fetchall()
    cursor.close()
    if rv[0][2] == requested_password :
        if requested_format =='json' or requested_format is None:
            return jsonify(),200
        elif requested_format == 'xml':
            return Response(status=200,mimetype='application/xml') 
    elif requested_format =='json' or requested_format is None:
        return jsonify(errors[0]),400
    elif requested_format == 'xml':
        return Response(error_toxml(errors[0]), status=400,mimetype='application/xml') 

@api_users.route('/application/register', methods=['POST'])
def new_user():
    requested_username = request.form['username']
    requested_password = request.form['password']
    requested_password_again = request.form['password_again']
    requested_format = request.args.get('format')

    if requested_password == requested_password_again:
        cursor = mysql.connection.cursor()
        cursor.execute(" SELECT COUNT(*) FROM user WHERE username =%s", (requested_username,))
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO user (username, password) VALUES (%s,%s)", (requested_username,requested_password))
            mysql.connection.commit()
            cursor.close()
            if requested_format =='json' or requested_format is None:
                return jsonify(), 201
            elif requested_format == 'xml':
                return Response(status=201,mimetype='application/xml') 
        elif requested_format =='json' or requested_format is None:
            return jsonify(errors[4]),409
        elif requested_format == 'xml':
            return Response(error_toxml(errors[4]), status=409,mimetype='application/xml') 

#GET ALL USER: GET /resources/users
#GET specified users: GET /resources/users?username
@api_users.route('/resources/users', methods=['GET'])
def users(*args):
    requested_username = request.args.get('username')
    requested_format = request.args.get('format')
    content = {}
    resDict = []
    if requested_username is None:
        cursor = mysql.connection.cursor()
        cursor.execute(" SELECT id, username FROM user")
        rv = cursor.fetchall()
        for col in rv:
            content = {"userdata":[{"id": col[0], "username": col[1]}]}
            resDict.append(content)
            content = {}
        if requested_format =='json' or requested_format is None:
            return jsonify(resDict)
        elif requested_format == 'xml':
            return Response(users_to_xml(resDict), mimetype='application/xml') 
    else:
        cursor = mysql.connection.cursor()
        cursor.execute(" SELECT id, username FROM user WHERE username =%s", (requested_username,))
        rv = cursor.fetchall()
        for col in rv:
            content = {"userdata":[{"id": col[0], "username": col[1]}]}
            resDict.append(content)
            content = {}
        if requested_format == 'json' or requested_format is None:
            if len(resDict) ==0:
                return jsonify(errors[2]), 404
            return jsonify(resDict)
        elif requested_format == 'xml':
            if len(resDict) ==0:
                return Response(error_toxml(errors[2]), status=404,mimetype='application/xml')  
            return Response(users_to_xml(resDict), mimetype='application/xml') 
