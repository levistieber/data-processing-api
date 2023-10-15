from flask import Blueprint, request, redirect, request, url_for, flash, Response, make_response, jsonify
from database import db
from models import Place, User
import validator
from response_builder import get_place, get_places, get_places_xml, get_place_response, get_place_xml, error_toxml
from errors import errors_dic, custom_errors_dic

place_blueprint = Blueprint('place_blueprint', __name__)

#Define possible content types in variables
contents_xml = ('application/xml', 'text/xml')
content_json = ('application/json')

#GET place
@place_blueprint.route('/api/resources/place')
def place():
    #Get the 'id' parameter from the request's query parameters
    request_id = request.args.get('id')

    #Save the content type of the request in a variable
    content_type = request.content_type

    #Check if 'id' is not present in the request
    if request_id is None:
        #Retrieve all places from database
        result = Place.query.all()
        
        if content_type == content_json:
            #Validate JSON response with JSON schema, return error if invalid
            if validator.validateJsonResponse(r'validators\json\get_place_schema.json', get_places(result)) is False:
                return make_response(jsonify(custom_errors_dic[0]), 400)
            #Return JSON response with a list of places
            return make_response(jsonify(get_places(result)), 200)
        
        elif content_type in contents_xml:
            #Validate XML response with XML schema, return error if invalid
            if validator.validateXmlResponse(r'validators\xml\get_place_schema.xsd', get_places_xml(result)) is False:
                return Response(error_toxml(custom_errors_dic[0]), mimetype='text/xml', status=400)
            #Return XML response with a list of places
            return Response(get_places_xml(result), mimetype='text/xml',status=200)
    else:
        #Database query place by id
        result = Place.query.filter_by(id=request_id).first()
        if content_type == content_json:
            #Validate JSON response with JSON schema, return error if invalid
            if validator.validateJsonResponse(r'validators\json\get_place_schema.json', get_place(result)) is False:
                return make_response(jsonify(custom_errors_dic[0]), 400)
            #Return JSON response with the specific place
            return make_response(jsonify(get_place(result)), 200)
        elif content_type in contents_xml:
            #Validate XML response with XML schema, return error if invalid
            if validator.validateXmlResponse(r'validators\xml\get_place_schema.xsd', get_place_xml(result)) is False:
                return Response(error_toxml(custom_errors_dic[0]), mimetype='text/xml', status=400)
            #Return XML response with the specific place
            return Response(get_place_xml(result), mimetype='text/xml',status=200)

#POST place
@place_blueprint.route('/api/resources/place', methods=['POST'])
def place_post():
    #Save the content type of the request in a variable
    content_type = request.content_type
    
    if content_type == content_json:
        #Validate JSON response with JSON schema, return error if invalid
        if validator.validateJsonResponse(r'validators\json\post_put_place.json', request.json) is False:
            return make_response(jsonify(custom_errors_dic[0]), 400)
        
        #Extract relevant data from the JSON request
        name = list(request.json.get('place'))[0]
        latitude = request.json.get('place').get(name).get('coordinates').get('latitude', None)
        longitude = request.json.get('place').get(name).get('coordinates').get('longitude', None)

        #Check if required data is missing and respond with an error
        if not name or not latitude or not longitude:
            return make_response(jsonify(errors_dic[7]), 422)
        
    elif content_type in contents_xml:
        #Validate XML response with XML schema, return error if invalid
        if validator.validateXmlResponse(r'validators\xml\post_put_place.xsd', request.data) is False:
            return Response(error_toxml(custom_errors_dic[0]), mimetype='text/xml', status=400)

        #Extract relevant data from the XML request
        name = list(get_place_response(request.data)['place'])[0]
        latitude = get_place_response(request.data)['place'][name]['coordinates']['latitude']
        longitude = get_place_response(request.data)['place'][name]['coordinates']['longitude']

        #Check if required data is missing and respond with an error
        if not name or not latitude or not longitude:
            return Response(error_toxml(errors_dic[7]), mimetype='text/xml', status=422)

    #If content type is not recognized, return an appropriate response
    else:
        return make_response(jsonify(errors_dic[6]), 415)

    #Check if a place with the same name already exists in the database
    exist = Place.query.filter_by(name=name).first()
    #Return error response if place already exists
    if exist:
        if content_type == content_json:
            return make_response(jsonify(errors_dic[4]), 409)
        elif content_type in contents_xml:
            return Response(error_toxml(errors_dic[4]), mimetype='text/xml', status=409)

    #Create a new Place object and add it to the database
    new_place = Place(name=name, latitude=latitude, longitude=longitude)
    db.session.add(new_place)
    db.session.commit()

    #Return a success response based on the content type
    if content_type == content_json:
        return Response('Place added successfully!',mimetype='application/json',status=201)
    if content_type in contents_xml:
        return Response('Place added successfully!',mimetype='text/xml',status=201)

#UPDATE place
@place_blueprint.route('/api/resources/place', methods=['PUT'])
def place_put():
    #Get the 'id' parameter from the request's query parameters
    request_id = request.args.get('id')

    #Save the content type of the request in a variable
    content_type = request.content_type

    #Error response if id is not present in request
    if request_id is None:
        if content_type == 'application/json':
            return make_response(jsonify(errors_dic[0]), 400)
        elif content_type in contents_xml:
            return Response(error_toxml(errors_dic[0]), mimetype='text/xml', status=400)
        
    #If id is present
    else:
        #Retrieve the place to be updated based on the provided 'id'
        update = Place.query.filter_by(id=request_id).first()
        name, latitude, longitude = None, None, None

        if content_type == content_json:
            #Validate JSON response with JSON schema, return error if invalid
            if validator.validateJsonResponse(r'validators\json\post_put_place.json', request.json) is False:
                return make_response(jsonify(custom_errors_dic[0]), 400)
            #Extract relevant data from the JSON request
            name = list(request.json.get('place'))[0]
            latitude = request.json.get('place').get(name).get('coordinates').get('latitude', None)
            longitude = request.json.get('place').get(name).get('coordinates').get('longitude', None)
            
        elif content_type in contents_xml:
            #Validate XML response with XML schema, return error if invalid
            if validator.validateXmlResponse(r'validators\xml\post_put_place.xsd', request.data) is False:
                return Response(error_toxml(custom_errors_dic[0]), mimetype='text/xml', status=400)
            #Extract relevant data from the XML request
            name = list(get_place_response(request.data)['place'])[0]
            latitude = get_place_response(request.data)['place'][name]['coordinates']['latitude']
            longitude = get_place_response(request.data)['place'][name]['coordinates']['longitude']

        #Error response if request content type is wrong
        else:
            return Response('Wrong content type!',mimetype='application/json', status=400)

        #Check if the place to be updated exists. If not, return error response
        if update is None:
            if content_type == content_json:
                return make_response(jsonify(errors_dic[2]), 404)
            if content_type in contents_xml:
                return Response(error_toxml(errors_dic[2]), mimetype='text/xml', status=404)

        #Check if the parameters to be updated are set. If yes, update those
        if name is not None:
             update.name = name
        if latitude is not None:
            update.latitude = latitude
        if longitude is not None:
            update.longitude = longitude

        #Commit changes to database
        db.session.commit()

        #Success response
        if content_type == content_json:
            return Response('Place updated successfully!',mimetype='application/json')
        if content_type in contents_xml:
            return Response('Place updated successfully!',mimetype='text/xml')
    
#DELETE place
@place_blueprint.route('/api/resources/place', methods=['DELETE'])
def place_delete():
    #Get the 'id' parameter from the request's query parameters
    request_id = request.args.get('id')

    #Save the content type of the request in a variable
    content_type = request.content_type

    #Check if id is not present in request
    if request_id is None:
        if content_type == content_json:
            return make_response(jsonify(errors_dic[0]), 400)
        elif content_type in contents_xml:
            return Response(error_toxml(errors_dic[0]), mimetype='text/xml', status=400)

    #If id is present
    else:
        #Query the place to be deleted based on the provided 'id'
        place = Place.query.filter_by(id=request_id)

        #Check if the place exists, if not, error response 404
        if place is None:
            if content_type == content_json:
                return make_response(jsonify(errors_dic[2]), 404)
            else if content_type in contents_xml:
                return Response(error_toxml(errors_dic[2]), mimetype='text/xml', status=404)

        #If place exists, delete it and commit changes to database
        place.delete()
        db.session.commit()

        #Success response
        if content_type == content_json:
            return Response('Place deleted successfully!',mimetype='application/json')
        else if content_type in contents_xml:
            return Response('Place deleted successfully!',mimetype='text/xml')
