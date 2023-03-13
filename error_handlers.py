from xml.dom.minidom import parseString
from xml.etree.ElementTree import Element,tostring
from flask import Response
from flask import request, jsonify
from toxml import *
from errors import *

from flask import Blueprint

error_handlers = Blueprint('error_handlers', __name__)

#error handlers
@error_handlers.errorhandler(400)
def not_allowed(e):
    if request.args.get('format') == 'json' or request.args.get('format') is None:
        return jsonify(errors[0]), 400
    elif request.args.get('format') == 'xml':
        return Response(error_toxml(errors[0]), status=400,mimetype='application/xml')  

@error_handlers.errorhandler(401)
def not_allowed(e):
    if request.args.get('format') == 'json' or request.args.get('format') is None:
        return jsonify(errors[1]), 401
    elif request.args.get('format') == 'xml':
        return Response(error_toxml(errors[1]), status=401,mimetype='application/xml')  

@error_handlers.errorhandler(404)
def not_found(e):
    if request.args.get('format') == 'json' or request.args.get('format') is None:
        return jsonify(errors[2]), 404
    elif request.args.get('format') == 'xml':
        return Response(error_toxml(errors[2]), status=404,mimetype='application/xml') 

@error_handlers.errorhandler(405)
def not_allowed(e):
    if request.args.get('format') == 'json' or request.args.get('format') is None:
        return jsonify(errors[3]), 405
    elif request.args.get('format') == 'xml':
        return Response(error_toxml(errors[3]), status=405,mimetype='application/xml') 

@error_handlers.errorhandler(409)
def not_allowed(e):
    if request.args.get('format') == 'json' or request.args.get('format') is None:
        return jsonify(errors[4]), 409
    elif request.args.get('format') == 'xml':
        return Response(error_toxml(errors[4]), status=409,mimetype='application/xml')  

@error_handlers.errorhandler(410)
def not_allowed(e):
    if request.args.get('format') == 'json' or request.args.get('format') is None:
        return jsonify(errors[5]), 410
    elif request.args.get('format') == 'xml':
        return Response(error_toxml(errors[5]), status=410,mimetype='application/xml') 

@error_handlers.errorhandler(415)
def not_allowed(e):
    if request.args.get('format') == 'json' or request.args.get('format') is None:
        return jsonify(errors[6]), 415
    elif request.args.get('format') == 'xml':
        return Response(error_toxml(errors[6]), status=415,mimetype='application/xml')  

@error_handlers.errorhandler(422)
def not_allowed(e):
    if request.args.get('format') == 'json' or request.args.get('format') is None:
        return jsonify(errors[7]), 422
    elif request.args.get('format') == 'xml':
        return Response(error_toxml(errors[7]), status=422,mimetype='application/xml') 

@error_handlers.errorhandler(500)
def not_allowed(e):
    if request.args.get('format') == 'json' or request.args.get('format') is None:
        return jsonify(errors[8]), 500
    elif request.args.get('format') == 'xml':
        return Response(error_toxml(errors[8]), status=500,mimetype='application/xml') 