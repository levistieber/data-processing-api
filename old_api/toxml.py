import re
from xml.etree.ElementTree import Element,tostring

testdict = [{
    'id':'17',
    'name':'Emmen around',
    'start_id':'19',
    'end_id':'20'
},
{
    'id':'18',
    'name':'In Emmen',
    'start_id':'19',
    'end_id':'20'
}]
testdictone = [{
    'id':'17',
    'name':'Emmen around',
    'start_id':'19',
    'end_id':'20'
}]

def fav_to_xml(d):
    
    root = Element('routes')
    
    for item in d:
        elem = Element('route')
        elem.set('id',str(item['id']))
        name = Element('name')
        places = Element('places')
        start_id = Element('start_id')
        end_id = Element('end_id')


        name.text= str(item['name'])
        start_id.text =str(item['places'][0]['start_id'])
        end_id.text= str(item['places'][0]['end_id'])

        places.append(start_id)
        places.append(end_id)

        elem.append(name)
        elem.append(places)

        root.append(elem)

    print(tostring(root))
    return tostring(root,encoding='UTF-8', method='xml')

def places_to_xml(d):

    root =Element('places')

    for item in d:
        elem = Element('place')
        elem.set('id',str(item['id']))

        name = Element('name')
        coordinates = Element('coordinates')
        latitude = Element('latitude')
        longitude = Element('longitude')

        name.text = str(item['name'])
        latitude.text = str(item['coordinates'][0]['latitude'])
        longitude.text = str(item['coordinates'][0]['longitude'])
        
        coordinates.append(latitude)
        coordinates.append(longitude)

        elem.append(name)
        elem.append(coordinates)
        root.append(elem)
    
    return tostring(root,encoding='UTF-8', method='xml')

def users_to_xml(d):

    root = Element('users')

    for item in d:
        
        elem = Element('user')
        elem.set('id', str(item['userdata'][0]['id']))
        username = Element('username')
        
        username.text=str(item['userdata'][0]['username'])

        elem.append(username)
        root.append(elem)
    
    return tostring(root,encoding='UTF-8', method='xml')

def error_toxml(d):

    root = Element('response')
    root.set('status', str(d['response']['error'][0]['status']))

    error = Element('error')
    message = Element('message')

    error.set ( 'name', str(d['response']['error'][0]['name']))
    message.text = str(d['response']['error'][0]['message'])

    error.append(message)
    root.append(error)

    return tostring(root,encoding='UTF-8', method='xml')

        