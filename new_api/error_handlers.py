from flask import Blueprint,Response,request, jsonify, make_response
from response_builder import error_toxml
from errors import errors_dic
error_handlers = Blueprint('error_handlers', __name__)

#error handlers
@error_handlers.errorhandler(400)
def not_allowed(e):
    if request.content_type == 'application/json':
        return make_response(jsonify(errors_dic[0]), 400)
    else:
        return Response(error_toxml(errors_dic[0]), mimetype='text/xml', status=400) 

@error_handlers.errorhandler(401)
def not_allowed(e):
    if request.content_type == 'application/json':
        return make_response(jsonify(errors_dic[1]), 401)
    else:
        return Response(error_toxml(errors_dic[1]), mimetype='text/xml', status=401) 

@error_handlers.errorhandler(404)
def not_found(e):
    if request.content_type == 'application/json':
        return make_response(jsonify(errors_dic[2]), 404)
    else:
        return Response(error_toxml(errors_dic[2]), mimetype='text/xml', status=404) 

@error_handlers.errorhandler(405)
def not_allowed(e):
    if request.content_type == 'application/json':
        return make_response(jsonify(errors_dic[3]), 405)
    else:
        return Response(error_toxml(errors_dic[3]), mimetype='text/xml', status=405) 

@error_handlers.errorhandler(409)
def not_allowed(e):
    if request.content_type == 'application/json':
        return make_response(jsonify(errors_dic[4]), 409)
    else:
        return Response(error_toxml(errors_dic[4]), mimetype='text/xml', status=409) 

@error_handlers.errorhandler(410)
def not_allowed(e):
    if request.content_type == 'application/json':
        return make_response(jsonify(errors_dic[5]), 410)
    else:
        return Response(error_toxml(errors_dic[5]), mimetype='text/xml', status=410) 

@error_handlers.errorhandler(415)
def not_allowed(e):
    if request.content_type == 'application/json':
        return make_response(jsonify(errors_dic[6]), 415)
    else:
        return Response(error_toxml(errors_dic[6]), mimetype='text/xml', status=415) 

@error_handlers.errorhandler(422)
def not_allowed(e):
    if request.content_type == 'application/json':
        return make_response(jsonify(errors_dic[7]), 422)
    else:
        return Response(error_toxml(errors_dic[7]), mimetype='text/xml', status=422) 

@error_handlers.errorhandler(500)
def not_allowed(e):
    if request.content_type == 'application/json':
        return make_response(jsonify(errors_dic[8]), 500)
    else:
        return Response(error_toxml(errors_dic[8]), mimetype='text/xml', status=500) 