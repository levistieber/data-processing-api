from flask import Blueprint, request, redirect, request, url_for, flash, Response, jsonify, make_response
from database import db
from models import Route
import validator
from response_builder import get_route, get_routes, get_route_xml, get_routes_xml, get_route_response, error_toxml
from errors import errors_dic, custom_errors_dic

route_blueprint = Blueprint('route_blueprint', __name__)

#GET route
@route_blueprint.route('/api/resources/user/route')
def route():
    #Get the 'id' parameter from the request's query parameters
    request_id = request.args.get('id')

    #Save the content type of the request in a variable
    content_type = request.content_type

    #Define possible content types in variables
    contents_xml = ('application/xml', 'text/xml')
    content_json = ('application/json')

    #Check if id is not present in request
    if request_id is None:
        #Retrieve all routes
        result = Route.query.all()
        
        if content_type == content_json:
            #Validate json response with schema
            if validator.validateJsonResponse(r'validators\json\get_route_schema.json', get_routes(result)) is False:
                #Return error response
                return make_response(jsonify(custom_errors_dic[0]), 400)
            #Return json response with list of routes
            return make_response(jsonify(get_routes(result)), 200)
        
        elif content_type in contents_xml:
            #Validate xml response with schema
            if validator.validateXmlResponse(r'validators\xml\get_route_schema.xsd', get_routes_xml(result)) is False:
                #Return error response
                return Response(error_toxml(custom_errors_dic[0]), mimetype='text/xml', status=400)
            #Return xml response with list of routes
            return Response(get_routes_xml(result), mimetype='text/xml',status=200)
    else:
        #Retrieve specific route by id
        result = Route.query.filter_by(id=request_id).first()
        
        if content_type == content_json:
            #Validate json response with schema
            if validator.validateJsonResponse(r'validators\json\get_route_schema.json', get_route(result)) is False:
                #Return error response
                return make_response(jsonify(custom_errors_dic[0]), 400)
            #Return json response with the specific route
            return make_response(jsonify(get_route(result)), 200)
        
        elif content_type in contents_xml:
            #Validate xml response with schema
            if validator.validateXmlResponse(r'validators\xml\get_route_schema.xsd', get_route_xml(result)) is False:
                #Return error response
                return Response(error_toxml(custom_errors_dic[0]), mimetype='text/xml', status=400)
            #Return xml response with the specific route
            return Response(get_route_xml(result), mimetype='text/xml',status=200)
        
#POST route
@route_blueprint.route('/api/resources/user/route', methods=['POST'])
def route_post():
    #Save the content type of the request in a variable
    content_type = request.content_type

    #Define possible content types in variables
    contents_xml = ('application/xml', 'text/xml')
    content_json = ('application/json')
    
    if content_type == content_json:
        #Validate json response with schema
        if validator.validateJsonResponse(r'validators\json\post_put_route_schema.json', request.json) is False:
            #Return error response
            return make_response(jsonify(custom_errors_dic[0]), 400)
        #Extract relevant data from the JSON request
        name = list(request.json.get('route'))[0]
        start = request.json.get('route').get(name).get('locations').get('start_id', None)
        end = request.json.get('route').get(name).get('locations').get('end_id', None)
        user_id = request.json.get('route').get(name).get('user_id',None)
        #Check if any required data is missing and respond with an error
        if not name or not start or not end or not user_id:
            return make_response(jsonify(errors_dic[7]), 422)

    elif content_type in contents_xml:
        #Validate xml response with schema
        if validator.validateXmlResponse(r'validators\xml\post_put_route_schema.xsd', request.data) is False:
            #Return error response
            return Response(error_toxml(custom_errors_dic[0]), mimetype='text/xml', status=400)
        #Extract relevant data from the XML request
        name = get_route_response(request.data)['route']['name']
        start = get_route_response(request.data)['route']['locations']['start_id']
        end = get_route_response(request.data)['route']['locations']['end_id']
        user_id = get_route_response(request.data)['route']['user_id']
        #Check if any required data is missing and respond with an error
        if not name or not start or not end or not user_id:
            return Response(error_toxml(errors_dic[7]), mimetype='text/xml', status=422)
        
    #If content type is not recognized, return an error response
    else:
        return make_response(jsonify(errors_dic[6]), 415)

    #Create a new Route object and add it to the database
    new_route = Route(name=name, start_id=start, end_id=end, user_id=user_id)
    db.session.add(new_route)
    db.session.commit()

    #Return a success response based on the content type
    if content_type == content_json:
        return Response('Route added successfully!',mimetype='application/json',status=201)
    if content_type in contents_xml:
        return Response('Route added successfully!',mimetype='text/xml',status=201)
    
#UPDATE place
@route_blueprint.route('/api/resources/user/route', methods=['PUT'])
def route_put():
    #Get the 'id' parameter from the request's query parameters
    request_id = request.args.get('id')

    #Save the content type of the request in a variable
    content_type = request.content_type

    #Define possible content types in variables
    contents_xml = ('application/xml', 'text/xml')
    content_json = ('application/json')

    #Check if id is not present in request. Error response if not
    if request_id is None:
        if content_type == content_json:
            return make_response(jsonify(errors_dic[0]), 400)
        else if content_type in contents_xml:
            return Response(error_toxml(errors_dic[0]), mimetype='text/xml', status=400)
        
    else:
        #Retrieve the route to be updated based on the provided 'id'
        update = Route.query.filter_by(id=request_id).first()
        
        name, start, end, user_id = None, None, None, None
        
        if content_type == content_json
            #Validate json response with schema
            if validator.validateJsonResponse(r'validators\json\post_put_route_schema.json', request.json) is False:
                #Return error response
                return make_response(jsonify(custom_errors_dic[0]), 400)
            #Extract parameters from request
            name = list(request.json.get('route'))[0]
            start = request.json.get('route').get(name).get('locations').get('start_id', None)
            end = request.json.get('route').get(name).get('locations').get('end_id', None)
            user_id = request.json.get('route').get(name).get('user_id',None)
            
        elif content_type in contents_xml:
            #Validate xml response with schema
            if validator.validateXmlResponse(r'validators\xml\post_put_route_schema.xsd', request.data) is False:
                #Return error response
                return Response(error_toxml(custom_errors_dic[0]), mimetype='text/xml', status=400)
            #Extract parameters from request
            name = get_route_response(request.data)['route']['name']
            start = get_route_response(request.data)['route']['locations']['start_id']
            end = get_route_response(request.data)['route']['locations']['end_id']
            user_id = get_route_response(request.data)['route']['user_id']
            
        else:
            #If content type is not recognized, return an error response
            return make_response(jsonify(errors_dic[6]), 415)

        #Check if the route to be updated exists. If not, return error message
        if update is None:
            if content_type == content_json:
                return make_response(jsonify(errors_dic[2]), 404)
            if content_type in contents_xml:
                return Response(error_toxml(errors_dic[2]), mimetype='text/xml', status=404)

        #Update route info where it changed
        if name is not None:
            update.name = name
        if start is not None:
            update.start_id = start
        if end is not None:
                update.end_id = end
        if user_id is not None:
            update.user_id = user_id

        #Commit changes to database
        db.session.commit()

        #Success response
        if content_type == content_json:
            return Response('Route updated successfully!',mimetype='application/json')
        if content_type in contents_xml:
            return Response('Route updated successfully!',mimetype='text/xml')
        
#DELETE place
@route_blueprint.route('/api/resources/user/route', methods=['DELETE'])
def route_delete():
    #Get the 'id' parameter from the request's query parameters
    request_id = request.args.get('id')

    #Save the content type of the request in a variable
    content_type = request.content_type

    #Define possible content types in variables
    contents_xml = ('application/xml', 'text/xml')
    content_json = ('application/json')

    #Check if id is missing in the request, error response if missing
    if request_id is None:
        if content_type == 'application/json':
            return make_response(jsonify(errors_dic[0]), 400)
        else if content_type in contents_xml:
            return Response(error_toxml(errors_dic[0]), mimetype='text/xml', status=400)
    else:
        #Query route to delete by id
        route = Route.query.filter_by(id=request_id)
        
        if content_type == content_json:
            #Check if route exists, if not, error response
            if route is None:
                return make_response(jsonify(errors_dic[2]), 404)
            #If exists, delete route from database
            route.delete()
            db.session.commit()
            #Success response
            return Response('Route deleted',mimetype='application/json')
        elif content_type in contents_xml:
            #Check if route exists, if not, error response
            if route is None:
                return Response(error_toxml(errors_dic[2]), mimetype='text/xml', status=404)
            #If exists, delete route from database
            route.delete()
            db.session.commit()
            #Success response
            return Response('Route deleted',mimetype='text/xml')
