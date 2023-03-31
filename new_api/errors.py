errors_dic = [
    {   
        'response':{
            'error': [{
                'name': 'BadRequest',
                'message' : 'The request was malformed',
                'status' : 400
        }]
        }
    },
    {   
        'response':{
            'error': [{
                'name':'Unauthorized',
                'message' : 'The the client is not authorized to perform the requested action',
                'status' : 401
        }]
        }
    },
    {   
        'response':{
            'error': [{
                'name':'ResourceNotFound',
                'message' : 'The requested resource was not found.',
                'status' : 404
            }]
        }
    },
    {   
        'response':{
            'error': [{
                'name':'MethodNotAllowed',
                'message' : 'The method is not allowed for the requested URL',
                'status' : 405
        }]
        }
    },
    {   'response':{
            'error': [{
                'name':'ResourceAlreadyExistsError', 
                'message': "A resource with that name already exists.",
                'status': 409
        }]
        }
    },
    {   
        'response':{
            'error': [{
                'name':'ResourceDoesNotExist',
                'message': "A resource with that ID no longer exists.",
                'status': 410
        }]
        }
    },
    {   
        'response':{
            'error': [{
                'name':'UnsupportedMediaType',
                'message' : 'The requested media type is not supperted by the server.',
                'status' : 415
        }]
        }
    },
    {   
        'response':{
            'error': [{
                'name':'UnprocessableEntity',
                'message' : 'The requested data was properly formatted but contained invalid or missing data.',
                'status' : 422
        }]
        }
    },
    {   
        'response':{
            'error': [{
                'name':'InternalServerError',
                'message' : 'The server threw an error when processing the request',
                'status' : 500
        }]
        }
    }]

custom_errors_dic =[
    {
        'response':{
            'error': [{
                'name':'ValidationError', 
                'message': "Validation failed!",
                'status': 400
        }]
        }
    }]