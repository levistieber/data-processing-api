from xml.dom.minidom import parseString
from xml.etree.ElementTree import Element,tostring
from flask import Response
from flask import request, jsonify
from toxml import *
from errors import *
from api_mysql import mysql

from flask import Blueprint

api_places = Blueprint('api_places', __name__)

#GET ALL PLACES, SPECIFIED PLACE
#Specified place exmaple: /resources/places?id=15
@api_places.route('/resources/places', methods=['GET'])
def places(*args):
    li=[]
    for arg in args:
        li.append(arg)
    if len(li) ==0:
        requested_id = request.args.get('id')
        requested_format = request.args.get('format')
    elif len(li) ==1:
        requested_id = li[0]
    elif len(li) ==2:
        requested_id = li[0]
        requested_format = li[1]
        
    content = {}
    resDict = []
    if requested_id is None:
        cursor = mysql.connection.cursor()
        cursor.execute(" SELECT id, name, latitude, longitude FROM places")
        rv = cursor.fetchall()
        for col in rv:
            content = {"id": col[0], "name": col[1], "coordinates": [{"latitude": col[2], "longitude": col[3]}]}
            resDict.append(content)
            content = {}
        if requested_format == 'json' or requested_format is None:
            return jsonify(resDict)
        elif requested_format == 'xml':
            return(Response(places_to_xml(resDict),mimetype='application/xml'))
    else:
        cursor = mysql.connection.cursor()
        cursor.execute(" SELECT id, name, latitude, longitude FROM places WHERE id =%s", (requested_id,))
        rv = cursor.fetchall()
        for col in rv:
            content = {"id": col[0], "name": col[1], "coordinates": [{"latitude": col[2], "longitude": col[3]}]}
            resDict.append(content)
            content = {}
        if requested_format == 'json' or requested_format is None:
            if len(resDict) ==0:
                return jsonify(errors[2]),404
            return jsonify(resDict)
        elif requested_format == 'xml':
            if len(resDict) == 0:
                return Response(error_toxml(errors[2]), status=404,mimetype='application/xml') 
            return(Response(places_to_xml(resDict),mimetype='application/xml')) 

#url needs to be changed to /resources/places
#the methods itself will determine the action 
#POST is creating new row in the place table
@api_places.route('/resources/places', methods=['POST'])
def new_place(*args):
    requested_format = None; 
    li=[]
    for arg in args:
        li.append(arg)

    if len(li) ==0:
        place_name = 'Emmen'
        latitude = 10.3213
        longitude = 32.2313
        requested_format = request.args.get('format')
    elif len(li) == 3:
        place_name = li[0]
        latitude = li[1]
        longitude = li[2]
    elif len(li) == 4:
        place_name = li[0]
        latitude = li[1]
        longitude = li[2]
        requested_format = li[3]

    cursor = mysql.connection.cursor()
    cursor.execute(" SELECT COUNT(*) FROM places WHERE name =%s", (place_name,))
    data = cursor.fetchone()[0]
    if data == 0:
        cursor.execute("INSERT INTO places (name, latitude, longitude) VALUES (%s,%b,%b)", (place_name, latitude, longitude))
        mysql.connection.commit()
        cursor.close()
        if requested_format == 'json' or requested_format is None:
            return jsonify(), 201
        elif requested_format == 'xml':
            return Response(status=201,mimetype='application/xml') 
    else:
        cursor.execute(" SELECT * FROM places WHERE name =%s", (place_name,))
        fetch = cursor.fetchall()
        for col in fetch:
            print(col[2])
            print(col[3])
            print(latitude)
            print(longitude)
            if float(col[2]) == float(latitude) and float(col[3]) == float(longitude):
                if requested_format == 'json' or requested_format is None:
                    return jsonify(), 201
                elif requested_format == 'xml':
                    return Response(status=201,mimetype='application/xml') 
            else:
                if requested_format == 'json' or requested_format is None:
                    return jsonify(custom_errors[1]), 409
                elif requested_format == 'xml':
                    return Response(error_toxml(custom_errors[1]), status=409,mimetype='application/xml')
