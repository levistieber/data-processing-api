import flask
from flask import Response, Blueprint
from flask import request, jsonify
from flask_mysqldb import MySQL
from errors import *
from api_mysql import mysql
from toxml import error_toxml

adminapi = Blueprint('adminapi', __name__)

#DELETE USER
@adminapi.route('/resources/users', methods=['DELETE'])
def delete_user():
    requested_username = request.args.get('username')
    requested_format = request.args.get('format')

    cursor = mysql.connection.cursor()
    cursor.execute(" DELETE FROM user WHERE username =%s", (requested_username,))
    mysql.connection.commit()
    if cursor.rowcount == 1:
        if requested_format == 'json':
            return Response(status=204)
        elif requested_format == 'xml':
            return Response(status=204, mimetype='application/xml')
    else:
        if requested_format == 'json':
            return jsonify(errors[0]), 400
        elif requested_format == 'xml':
            return Response(error_toxml(errors[0]), status=400, mimetype='application/xml')

#UPDATE USER
@adminapi.route('/resources/users', methods=['PUT'])
def update_user():
    requested_username = request.args.get('username')
    requested_new_username = request.args.get('new_username')
    requested_format = request.args.get('format')

    cursor= mysql.connection.cursor()
    cursor.execute("UPDATE user SET username =%s WHERE username = %s", (requested_new_username, requested_username))
    mysql.connection.commit()
    if cursor.rowcount == 1:
        if requested_format == 'json':
            return Response(status=204)
        elif requested_format == 'xml':
            return Response(status=204, mimetype='application/xml')
    else:
        if requested_format == 'json':
            return jsonify(errors[0]), 400
        elif requested_format == 'xml':
            return Response(error_toxml(errors[0]), status=400, mimetype='application/xml')

#DELETE PLACE
@adminapi.route('/resources/places', methods=['DELETE'])
def delete_place():
    requested_place = request.args.get('place')
    requested_format = request.args.get('format')
    if requested_place is None:
        if requested_format == 'json':
            return jsonify(errors[2]), 404
        elif requested_format == 'xml':
            return Response(error_toxml(errors[2]), status=404, mimetype='application/xml')
    else:
        cursor = mysql.connection.cursor()
        cursor.execute(" DELETE FROM places WHERE name =%s", (requested_place,))
        mysql.connection.commit()
        if cursor.rowcount == 1:
            if requested_format == 'json':
                return Response(status=204)
            elif requested_format == 'xml':
                return Response(status=204, mimetype='application/xml')
        else:
            if requested_format == 'json':
                return jsonify(errors[0]), 400
            elif requested_format == 'xml':
                return Response(error_toxml(errors[0]), status=400, mimetype='application/xml')

#UPDATE PLACE
@adminapi.route('/resources/places', methods=['PUT'])
def update_place():
    requested_place = request.args.get('place')
    requested_new_place = request.args.get('new_place')
    requested_latitude = request.args.get('latitude')
    requested_longitude = request.args.get('longitude')
    requested_format = request.args.get('format')

    if requested_new_place is not None:
        if requested_latitude is not None:
            if requested_longitude is not None:
                cursor= mysql.connection.cursor()
                cursor.execute("UPDATE places SET name =%s, latitude =%b, longitude =%b WHERE name = %s", (requested_new_place, requested_latitude, requested_longitude, requested_place))
                mysql.connection.commit()
            else:
                cursor= mysql.connection.cursor()
                cursor.execute("UPDATE places SET name =%s, latitude =%b, WHERE name = %s", (requested_new_place, requested_latitude, requested_place))
                mysql.connection.commit()
        elif requested_longitude is not None:
            cursor= mysql.connection.cursor()
            cursor.execute("UPDATE places SET name =%s, longitude =%b WHERE name = %s", (requested_new_place, requested_longitude, requested_place))
            mysql.connection.commit()
        else:
            cursor= mysql.connection.cursor()
            cursor.execute("UPDATE places SET name =%s WHERE name = %s", (requested_new_place, requested_place))
            mysql.connection.commit()
    elif requested_latitude is not None:
        if requested_longitude is not None:
            cursor= mysql.connection.cursor()
            cursor.execute("UPDATE places SET latitude =%b, longitude =%b WHERE name = %s", (requested_latitude, requested_longitude, requested_place))
            mysql.connection.commit()
        else:
            cursor= mysql.connection.cursor()
            cursor.execute("UPDATE places SET latitude =%b WHERE name = %s", (requested_latitude, requested_place))
            mysql.connection.commit()
    elif requested_longitude is not None:
        cursor= mysql.connection.cursor()
        cursor.execute("UPDATE places SET longitude =%b WHERE name = %s", (requested_longitude, requested_place))
        mysql.connection.commit()

    if cursor.rowcount == 1:
        if requested_format == 'json':
            return Response(status=204)
        elif requested_format == 'xml':
            return Response(status=204, mimetype='application/xml')
    else:
        if requested_format == 'json':
            return jsonify(errors[0]), 400
        elif requested_format == 'xml':
            return Response(error_toxml(errors[0]), status=400, mimetype='application/xml')
