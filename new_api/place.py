from flask import Blueprint, request, redirect, request, url_for, flash, Response, make_response, jsonify
from database import db
from models import Place, User
from response_builder import get_place, get_places, get_places_xml, get_place_response, get_place_xml

place_blueprint = Blueprint('place_blueprint', __name__)

#GET place
@place_blueprint.route('/api/resources/place')
def place():
    request_id = request.args.get('id')
    
    if request_id is None:
        if request.content_type == 'application/json':
            result = Place.query.all()
            return make_response(jsonify(get_places(result)), 200)
            ##return Response(get_places(result),mimetype='application/json',status=200)
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            result = Place.query.all()
            return Response(get_places_xml(result), mimetype='text/xml',status=200)
    else:
        if request.content_type == 'application/json':
            result = Place.query.filter_by(id=request_id).first()
            return make_response(jsonify(get_place(result)), 200)
            ##return Response(get_place(result), mimetype='application/json',status=200)
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            result = Place.query.filter_by(id=request_id).first()
            return Response(get_place_xml(result), mimetype='text/xml',status=200)

#POST place
@place_blueprint.route('/api/resources/place', methods=['POST'])
def place_post():
    if request.content_type == 'application/json':
        name = list(request.json.get('place'))[0]
        ##latitude = request.json.get('place').get(list(request.json.get('place'))[0]).get('coordinates').get('latitude', None)
        latitude = request.json.get('place').get(name).get('coordinates').get('latitude', None)
        ##longitude = request.json.get('place').get(list(request.json.get('place'))[0]).get('coordinates').get('longitude', None)
        longitude = request.json.get('place').get(name).get('coordinates').get('longitude', None)
        if not name:
            return Response('Missing name!',mimetype='application/json', status=400)
        if not latitude:
            return Response('Missing latitude!',mimetype='application/json', status=400)
        if not longitude:
            return Response('Missing longitude!',mimetype='application/json', status=400)
    elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
        ##return get_place_response(request.data)
        name = list(get_place_response(request.data)['place'])[0]
        latitude = get_place_response(request.data)['place'][name]['coordinates']['latitude']
        longitude = get_place_response(request.data)['place'][name]['coordinates']['longitude']
        if not name:
            return Response('Missing name!',mimetype='text/xml',status=400)
        if not latitude:
            return Response('Missing latitude!',mimetype='text/xml',status=400)
        if not longitude:
            return Response('Missing longitude!',mimetype='text/xml',status=400)
    else:
        return Response('Wrong content type!',mimetype='application/json', status=400)
    new_place = Place(name=name, latitude=latitude, longitude=longitude)
    db.session.add(new_place)
    db.session.commit()
    if request.content_type == 'application/json':
        return Response('Place added!',mimetype='application/json',status=201)
    if request.content_type == 'application/xml' or request.content_type == 'text/xml':
        return Response('Place added!',mimetype='text/xml',status=201)

#UPDATE place
@place_blueprint.route('/api/resources/place', methods=['PUT'])
def place_put():
    request_id = request.args.get('id')
    
    if request_id is None:
        return 'No id', 400
    else:
        update = Place.query.filter_by(id=request_id).first()
        name= None
        latitude = None
        longitude = None
        if request.content_type == 'application/json':
            name = list(request.json.get('place'))[0]
            ##latitude = request.json.get('place').get(list(request.json.get('place'))[0]).get('coordinates').get('latitude', None)
            latitude = request.json.get('place').get(name).get('coordinates').get('latitude', None)
            ##longitude = request.json.get('place').get(list(request.json.get('place'))[0]).get('coordinates').get('longitude', None)
            longitude = request.json.get('place').get(name).get('coordinates').get('longitude', None)
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            ##return get_place_response(request.data)
            name = list(get_place_response(request.data)['place'])[0]
            latitude = get_place_response(request.data)['place'][name]['coordinates']['latitude']
            longitude = get_place_response(request.data)['place'][name]['coordinates']['longitude']
        else:
            return Response('Wrong content type!',mimetype='application/json', status=400)
        if name is not None:
             update.name = name
        if latitude is not None:
            update.latitude = latitude
        if longitude is not None:
                update.longitude = longitude
        db.session.commit()
        if request.content_type == 'application/json':
            return Response('Place updated',mimetype='application/json')
        if request.content_type == 'application/xml' or request.content_type == 'text/xml':
            return Response('Place updated',mimetype='text/xml')
    
#DELETE place
@place_blueprint.route('/api/resources/place', methods=['DELETE'])
def place_delete():
    request_id = request.args.get('id')
    if request_id is None:
        return 'No id', 400
    else:
        if request.content_type == 'application/json':
            place = Place.query.filter_by(id=request_id)
            if place is None:
                return Response('Wrong ID',mimetype='application/json', status=400)
            place.delete()
            db.session.commit()
            return Response('Place deleted',mimetype='application/json')
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            place = Place.query.filter_by(id=request_id)
            if place is None:
                return Response('Wrong ID',mimetype='text/xml', status=400)
            place.delete()
            db.session.commit()
            return Response('Place deleted',mimetype='text/xml')
            
