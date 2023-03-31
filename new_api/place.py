from flask import Blueprint, request, redirect, request, url_for, flash, Response, make_response, jsonify
from database import db
from models import Place, User
import validator
from response_builder import get_place, get_places, get_places_xml, get_place_response, get_place_xml, error_toxml
from errors import errors_dic, custom_errors_dic

place_blueprint = Blueprint('place_blueprint', __name__)

#GET place
@place_blueprint.route('/api/resources/place')
def place():
    request_id = request.args.get('id')
    
    if request_id is None:
        if request.content_type == 'application/json':
            result = Place.query.all()
            if validator.validateJsonResponse(r'validators\json\get_place_schema.json', get_places(result)):
                return make_response(jsonify(custom_errors_dic[0]), 400)
            return make_response(jsonify(get_places(result)), 200)
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            result = Place.query.all()
            if validator.validateXmlResponse(r'validators\xml\get_place_schema.xsd', get_places_xml(result)) is False:
                return Response(error_toxml(custom_errors_dic[0]), mimetype='text/xml', status=400)
            return Response(get_places_xml(result), mimetype='text/xml',status=200)
    else:
        if request.content_type == 'application/json':
            result = Place.query.filter_by(id=request_id).first()
            if validator.validateJsonResponse(r'validators\json\get_place_schema.json', get_place(result)):
                return make_response(jsonify(custom_errors_dic[0]), 400)
            return make_response(jsonify(get_place(result)), 200)
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            result = Place.query.filter_by(id=request_id).first()
            if validator.validateXmlResponse(r'validators\xml\get_place_schema.xsd', get_place_xml(result)) is False:
                return Response(error_toxml(custom_errors_dic[0]), mimetype='text/xml', status=400)
            return Response(get_place_xml(result), mimetype='text/xml',status=200)

#POST place
@place_blueprint.route('/api/resources/place', methods=['POST'])
def place_post():
    if request.content_type == 'application/json':
        if validator.validateJsonResponse(r'validators\json\post_put_place.json', request.json):
            return make_response(jsonify(custom_errors_dic[0]), 400)
        name = list(request.json.get('place'))[0]
        latitude = request.json.get('place').get(name).get('coordinates').get('latitude', None)
        longitude = request.json.get('place').get(name).get('coordinates').get('longitude', None)
        if not name:
            return make_response(jsonify(errors_dic[7]), 422)
        if not latitude:
            return make_response(jsonify(errors_dic[7]), 422)
        if not longitude:
            return make_response(jsonify(errors_dic[7]), 422)
    elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
        if validator.validateXmlResponse(r'validators\xml\post_put_place.xsd', request.data) is False:
            return Response(error_toxml(custom_errors_dic[0]), mimetype='text/xml', status=400)
        name = list(get_place_response(request.data)['place'])[0]
        latitude = get_place_response(request.data)['place'][name]['coordinates']['latitude']
        longitude = get_place_response(request.data)['place'][name]['coordinates']['longitude']
        if not name:
            return Response(error_toxml(errors_dic[7]), mimetype='text/xml', status=422)
        if not latitude:
            return Response(error_toxml(errors_dic[7]), mimetype='text/xml', status=422)
        if not longitude:
            return Response(error_toxml(errors_dic[7]), mimetype='text/xml', status=422)
    else:
        return make_response(jsonify(errors_dic[6]), 415)
    exist = Place.query.filter_by(name=name).first()
    if exist:
        if request.content_type == 'application/json':
            return make_response(jsonify(errors_dic[4]), 409)
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            return Response(error_toxml(errors_dic[4]), mimetype='text/xml', status=409)
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
        if request.content_type == 'application/json':
            return make_response(jsonify(errors_dic[0]), 400)
        else:
            return Response(error_toxml(errors_dic[0]), mimetype='text/xml', status=400)
    else:
        update = Place.query.filter_by(id=request_id).first()
        name= None
        latitude = None
        longitude = None
        if request.content_type == 'application/json':
            if validator.validateJsonResponse(r'validators\json\post_put_place.json', request.json):
                return make_response(jsonify(custom_errors_dic[0]), 400)
            name = list(request.json.get('place'))[0]
            latitude = request.json.get('place').get(name).get('coordinates').get('latitude', None)
            longitude = request.json.get('place').get(name).get('coordinates').get('longitude', None)
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            if validator.validateXmlResponse(r'validators\xml\post_put_place.xsd', request.data) is False:
                return Response(error_toxml(custom_errors_dic[0]), mimetype='text/xml', status=400)
            name = list(get_place_response(request.data)['place'])[0]
            latitude = get_place_response(request.data)['place'][name]['coordinates']['latitude']
            longitude = get_place_response(request.data)['place'][name]['coordinates']['longitude']
        else:
            return Response('Wrong content type!',mimetype='application/json', status=400)
        if update is None:
            if request.content_type == 'application/json':
                return make_response(jsonify(errors_dic[2]), 404)
            if request.content_type == 'application/xml' or request.content_type == 'text/xml':
                return Response(error_toxml(errors_dic[2]), mimetype='text/xml', status=404)
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
        if request.content_type == 'application/json':
            return make_response(jsonify(errors_dic[0]), 400)
        else:
            return Response(error_toxml(errors_dic[0]), mimetype='text/xml', status=400)
    else:
        if request.content_type == 'application/json':
            place = Place.query.filter_by(id=request_id)
            if place is None:
                return make_response(jsonify(errors_dic[2]), 404)
            place.delete()
            db.session.commit()
            return Response('Place deleted',mimetype='application/json')
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            place = Place.query.filter_by(id=request_id)
            if place is None:
                return Response(error_toxml(errors_dic[2]), mimetype='text/xml', status=404)
            place.delete()
            db.session.commit()
            return Response('Place deleted',mimetype='text/xml')
            
