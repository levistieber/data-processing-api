from flask import Blueprint, request, redirect, request, url_for, flash, Response
from database import db
from models import Place, User
from response_builder import get_place, get_places, get_place_xml, get_place_response

place_blueprint = Blueprint('place_blueprint', __name__)

@place_blueprint.route('/api/resources/place')
def place():
    request_id = request.args.get('id')
    
    if request_id is None:
        if request.content_type == 'application/json':
            result = Place.query.all()
            return get_places(result)
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            result = Place.query.all()
            return Response(get_place_xml(result), mimetype='text/xml')
    else:
        if request.content_type == 'application/json':
            result = Place.query.filter_by(id=request_id).first()
            return get_place(result)
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            result = Place.query.filter_by(id=request_id).first()
            return Response(get_place_xml(result), mimetype='text/xml')
        
@place_blueprint.route('/api/resources/place', methods=['POST'])
def place_post():
    if request.content_type == 'application/json':
        name = request.json.get('name', None)
        latitude = request.json.get('latitude', None)
        longitude = request.json.get('longitude', None) 
    elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
        name = get_place_response(request.data)['place']['name']
        latitude = get_place_response(request.data)['place']['coordinates']['latitude']
        longitude = get_place_response(request.data)['place']['coordinates']['longitude']
        #return get_place_response(request.data) 
    if not name:
        return 'Missing name!', 400
    if not latitude:
        return 'Missing latitude!', 400
    if not longitude:
        return 'Missing longitude!', 400
    new_place = Place(name=name, latitude=latitude, longitude=longitude)
    db.session.add(new_place)
    db.session.commit()
    return 'Place added!', 201