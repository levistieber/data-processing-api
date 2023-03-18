from flask import Blueprint, request, redirect, request, url_for, flash, Response
from database import db
from models import Route
from response_builder import get_route, get_routes, get_route_xml, get_routes_xml, get_route_response

route_blueprint = Blueprint('place_routes', __name__)

#GET route
@route_blueprint.route('/api/resources/user/route')
def place():
    request_id = request.args.get('id')

    if request_id is None:
        if request.content_type == 'application/json':
            result = Route.query.all()
            return Response(get_routes(result),mimetype='application/json',status=200)
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            result = Route.query.all()
            return Response(get_routes_xml(result), mimetype='text/xml',status=200)
    else:
        if request.content_type == 'application/json':
            result = Route.query.filter_by(id=request_id).first()
            return Response(get_routes(result),mimetype='application/json',status=200)
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            result = Route.query.filter_by(id=request_id).first()
            return Response(get_routes_xml(result), mimetype='text/xml',status=200)
        
#POST route
@route_blueprint.route('/api/resources/user/route', methods=['POST'])
def place_post():
    if request.content_type == 'application/json':
        name = request.json.get('name', None)
        start = request.json.get('latitude', None)
        end = request.json.get('longitude', None)
        user_id = request.json.get('user_id',None)
        if not name:
            return Response('Missing name!',mimetype='application/json', status=400)
        if not start:
            return Response('Missing start location!',mimetype='application/json', status=400)
        if not end:
            return Response('Missing end location!',mimetype='application/json', status=400)
        if not user_id:
            return Response('Missing user!',mimetype='application/json', status=400)
    elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
        name = get_route_response(request.data)['route']['name']
        start = get_route_response(request.data)['route']['locations']['start']
        end = get_route_response(request.data)['route']['locations']['end']
        user_id = get_route_response(request.data)['route']['user_id']
        if not name:
            return Response('Missing name!',mimetype='application/json', status=400)
        if not start:
            return Response('Missing start location!',mimetype='application/json', status=400)
        if not end:
            return Response('Missing end location!',mimetype='application/json', status=400)
        if not user_id:
            return Response('Missing user!',mimetype='application/json', status=400)
    else:
        return Response('Wrong content type!',mimetype='application/json', status=400)
    new_route = Route(name=name, start_id=start, end_id=end, user_id=user_id)
    db.session.add(new_route)
    db.session.commit()
    if request.content_type == 'application/json':
        return Response('Route added!',mimetype='application/json',status=201)
    if request.content_type == 'application/xml' or request.content_type == 'text/xml':
        return Response('Route added!',mimetype='text/xml',status=201)
    
#UPDATE place
@route_blueprint.route('/api/resources/user/route', methods=['PUT'])
def place_put():
    request_id = request.args.get('id')
    
    if request_id is None:
        return 'No id', 400
    else:
        update = Route.query.filter_by(id=request_id).first()
        name = None
        start = None
        end = None
        user_id = None
        if request.content_type == 'application/json':
            name = request.json.get('name', None)
            start = request.json.get('latitude', None)
            end = request.json.get('longitude', None)
            user_id = request.json.get('user_id',None)
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            name = get_route_response(request.data)['route']['name']
            start = get_route_response(request.data)['route']['locations']['start']
            end = get_route_response(request.data)['route']['locations']['end']
            user_id = get_route_response(request.data)['route']['user_id']
        else:
            return Response('Wrong content type!',mimetype='application/json', status=400)
        if name is not None:
            update.name = name
        if start is not None:
            update.start_id = start
        if end is not None:
                update.end_id = end
        if user_id is not None:
            update.user_id = user_id
        db.session.commit()
        if request.content_type == 'application/json':
            return Response('Route updated',mimetype='application/json')
        if request.content_type == 'application/xml' or request.content_type == 'text/xml':
            return Response('Route updated',mimetype='text/xml')
        
#DELETE place
@route_blueprint.route('/api/resources/user/route', methods=['DELETE'])
def place_delete():
    request_id = request.args.get('id')
    if request_id is None:
        return 'No id', 400
    else:
        if request.content_type == 'application/json':
            place = Route.query.filter_by(id=request_id)
            if place is None:
                return Response('Wrong ID',mimetype='application/json', status=400)
            place.delete()
            db.session.commit()
            return Response('Place deleted',mimetype='application/json')
        elif request.content_type == 'application/xml' or request.content_type == 'text/xml':
            place = Route.query.filter_by(id=request_id)
            if place is None:
                return Response('Wrong ID',mimetype='text/xml', status=400)
            place.delete()
            db.session.commit()
            return Response('Place deleted',mimetype='text/xml')