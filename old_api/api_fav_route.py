from xml.dom.minidom import parseString
from xml.etree.ElementTree import Element,tostring
from flask import Response
from flask import request, jsonify
from toxml import *
from errors import *
from api_mysql import mysql
from api_places import new_place
from flask import Blueprint


api_fav_route = Blueprint('api_fav_route', __name__)


#GET ALL FAVOURITE ROUTES, SPECIFIED ROUTES
#Get all routes example: GET /resources/favourite
#Specified place example: GET /resources/favourite?id=15
#Ge all routes for specified user example: GET /resources/favourite?username=alekosz
@api_fav_route.route('/resources/favourite', methods=['GET'])
def routes():
    #requested_name = request.args.get('name')
    requested_id = request.args.get('id')
    requested_user = request.args.get('username')
    requested_format = request.args.get('format')
    content = {}
    resDict = []
    if requested_id is None and requested_user is None:
        cursor = mysql.connection.cursor()
        cursor.execute(" SELECT id, name, start_id, end_id FROM fav")
        rv = cursor.fetchall()
        for col in rv:
            content = {"id": col[0], "name": col[1], "places":[{"start_id": col[2], "end_id": col[3]}]}
            resDict.append(content)
            content = {}
        if requested_format == 'json' or requested_format is None:
            return jsonify(resDict)
        elif requested_format == 'xml':
            return Response(fav_to_xml(resDict), mimetype='application/xml')
    elif requested_user is not None and requested_id is None:
        cursor = mysql.connection.cursor()
        cursor.execute(" SELECT fav.id, fav.name, fav.start_id, fav.end_id FROM fav INNER JOIN user_fav_routes_connector ON fav.id = user_fav_routes_connector.fav_route_id INNER JOIN user ON user_fav_routes_connector.user_id = user.id WHERE user.username=%s", (requested_user,))
        rv = cursor.fetchall()
        for col in rv:
            content = {"id": col[0], "name": col[1], "places":[{"start_id": col[2], "end_id": col[3]}]}
            resDict.append(content)
            content = {}
        if requested_format == 'json' or requested_format is None:
            if len(resDict) ==0:
                return jsonify(errors[2]),404
            return jsonify(resDict)
        elif requested_format == 'xml':
            if len(resDict) ==0:
                return Response(error_toxml(errors[2]), status=404,mimetype='application/xml') 
            my_item_func = lambda x: 'route'
            return Response(fav_to_xml(resDict), mimetype='application/xml')
    elif requested_id is not None:
        cursor = mysql.connection.cursor()
        cursor.execute(" SELECT id, name, start_id, end_id FROM fav WHERE id =%s", (requested_id,))
        rv = cursor.fetchall()
        for col in rv:
            content = {"id": col[0], "name": col[1], "places":[{"start_id": col[2], "end_id": col[3]}]}
            resDict.append(content)
            content = {}
        if requested_format == 'json' or requested_format is None:
            if len(resDict) ==0:
                return jsonify(errors[2]),404
            return jsonify(resDict)
        elif requested_format == 'xml':
            if len(resDict) ==0:
                return Response(error_toxml(errors[2]), status=404,mimetype='application/xml') 
            return Response(fav_to_xml(resDict), mimetype='applicaiton/xml')


#NEW FAVOURITE ROUTE
#URL needs to be changed to /resources/favourite
#The method itself will determine the action
#Example for URL: POST /resources/favourite?format=json
#Values passed by form!
@api_fav_route.route('/resources/favourite', methods=['POST'])
def new_fav():
    username = request.form['username']
    route_name = request.form['route_name']
    start_place = request.form['start_place']
    start_latitude = request.form['start_latitude']
    start_longitude = request.form['start_longitude']
    end_place = request.form['end_place']
    end_latitude = request.form['end_latitude']
    end_longitude = request.form['end_longitude']
    requested_format = request.args.get('format')

    cursor = mysql.connection.cursor()
    cursor.execute(" SELECT COUNT(*) FROM fav WHERE name =%s", (route_name,))
    if cursor.fetchone()[0] == 0:
        if new_place(start_place, start_latitude, start_longitude)[1] == 201 and new_place(end_place, end_latitude, end_longitude)[1] == 201:
            cursor.execute("SELECT id from places WHERE name =%s", (start_place,))
            start_id = cursor.fetchone()[0]
            cursor.execute("SELECT id from places WHERE name =%s", (end_place,))
            end_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO fav (name, start_id, end_id) VALUES (%s,%b,%b)", (route_name, start_id, end_id))
            mysql.connection.commit()
            cursor.execute(" SELECT id FROM fav WHERE name =%s", (route_name,))
            fav_id = cursor.fetchone()[0]
            cursor.execute(" SELECT id FROM user WHERE username =%s", (username,))
            user_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO user_fav_routes_connector (user_id, fav_route_id) Values (%b,%b)", (user_id, fav_id))
            mysql.connection.commit()
            if requested_format == 'json' or requested_format is None:
                return jsonify(), 201
            if requested_format =='xml':
                return Response(status=201, mimetype='application/xml')
        elif requested_format == 'json' or requested_format is None:
            return jsonify(custom_errors[1]), 409
        elif requested_format =='xml':
            return Response(error_toxml(custom_errors[1]), status=409,mimetype='application/xml')
    else:
        if requested_format == 'json' or requested_format is None:
            return jsonify(custom_errors[0]), 409
        if requested_format =='xml':
            return Response(error_toxml(custom_errors[0]), status=409,mimetype='application/xml')
        

#DELETE FAVOURITE ROUTE
#URL needs to be changed to /resources/favourite
#THe method itself will determine the action
#Example for url: DELETE /resources/favourite?id=15&format=json
@api_fav_route.route('/resources/favourite', methods=['DELETE'])
def delete_fav():
    requested_format = request.args.get('format')
    requested_id = request.args.get('id')
    cursor = mysql.connection.cursor()
    cursor.execute(" DELETE FROM fav WHERE id =%b", (requested_id,))
    mysql.connection.commit()
    if cursor.rowcount == 1:
        if requested_format == 'json' or requested_format is None:
           return Response(status=204)
        elif requested_format =='xml':
            return Response(status=204, mimetype='application/xml')
    else:
        if requested_format == 'json' or requested_format is None:
           return jsonify(errors[2]),404
        elif requested_format =='xml':
            return Response(error_toxml(errors[2]), status=404,mimetype='application/xml') 

#UPDATE FAVOURITE ROUTE
#URL needs to be changed to /resources/favourite
#THe method itself will determine the action
#Example for url: UPDATE /resources/favourite?id=16&name=newname&format=json
@api_fav_route.route('/resources/favourite', methods=['PUT'])
def update_fav():
    requested_id = request.args.get('id')
    requested_name = request.form['name']
    requested_format = request.args.get('format')

    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE fav SET fav.name =%s WHERE fav.id=%b",(requested_name, requested_id))
    mysql.connection.commit()

    if cursor.rowcount == 1:
        if requested_format == 'json' or requested_format is None:
            return Response(status=204)
        elif requested_format == 'xml':
            return Response(status=204, mimetype='application/xml')
    else:
        if requested_format == 'json' or requested_format is None:
            return jsonify(errors[0]), 400
        elif requested_format == 'xml':
            return Response(error_toxml(errors[0]), status=400,mimetype='application/xml')
        