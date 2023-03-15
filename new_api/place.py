from flask import Blueprint, request, redirect, request, url_for, flash, Response
from database import db
from models import Place, User
from response_builder import get_place, get_places, get_place_xml

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