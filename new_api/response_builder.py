import re
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, tostring

#AUTH BUILDER
def credentials(xml):
    tree = ET.fromstring(xml)
    cred_dic={'credentials':{}}
    for node in tree.iter('credentials'):
        for elem in node.iter():
            if not elem.tag==node.tag:
                cred_dic['credentials'][elem.tag] = elem.text
    return cred_dic

def signup_request(xml):
    tree = ET.fromstring(xml)
    user_dic={'user':{}}
    inner_dic = {}
    name = None
    for node in tree.iter('user'):
        for elem in node:
            if not elem.tag==node.tag:
                if elem:
                    inner_dic[name][elem.tag] = recursive(elem)
                else:
                    if elem.tag == 'name':
                        name = elem.text
                        inner_dic = {elem.text :{}}
                    inner_dic[name][elem.tag] = elem.text
    user_dic['user'].update(inner_dic)
    return user_dic

#USER BUILDER
def get_user(result):
    usrs = {'users':[]}
    usr = {
        result.name:{
            'id': (result.id),
            'credentials':{
                'email': (result.email),
                'password': str(result.password)
            }
        }
    }
    usrs['users'].append(usr)
    return usrs

def get_users(result):
    usrs = {'users':[]}
    for row in result:
        usr = {
            row.name:{
                'id': (row.id),
                'credentials':{
                    'email': (row.email),
                    'password': str(row.password)
                }
            }
        }
        usrs['users'].append(usr)
    return usrs

def get_user_xml(row):
    root =Element('users')

    elem = Element('user')
    elem.set('id',str(row.id))

    name = Element('name')
    credentials = Element('credentials')
    email = Element('email')
    password = Element('password')

    name.text = row.name
    email.text = str(row.email)
    password.text = str(row.password)
        
    credentials.append(email)
    credentials.append(password)

    elem.append(name)
    elem.append(credentials)
    root.append(elem)
    
    return tostring(root, encoding='UTF-8', method='xml', xml_declaration=True)

def get_users_xml(result):
    root =Element('users')
    for row in result:
        elem = Element('user')
        elem.set('id',str(row.id))

        name = Element('name')
        credentials = Element('credentials')
        email = Element('email')
        password = Element('password')

        name.text = row.name
        email.text = str(row.email)
        password.text = str(row.password)
        
        credentials.append(email)
        credentials.append(password)

        elem.append(name)
        elem.append(credentials)
        root.append(elem)
    
    return tostring(root, encoding='UTF-8', method='xml', xml_declaration=True)

#PLACE BUILDER
def get_place(result):
    plcs = {'places':[]}
    plc = {
        result.name:{
            'id': (result.id),
            'coordinates':{
                'latitude': (result.latitude),
                'longitude': (result.longitude)
            }
        }
    }
    plcs['places'].append(plc)
    return plcs

def get_place_xml(row):
    root =Element('places')

    elem = Element('place')
    elem.set('id',str(row.id))

    name = Element('name')
    coordinates = Element('coordinates')
    latitude = Element('latitude')
    longitude = Element('longitude')

    name.text = row.name
    latitude.text = str(row.latitude)
    longitude.text = str(row.longitude)
        
    coordinates.append(latitude)
    coordinates.append(longitude)

    elem.append(name)
    elem.append(coordinates)
    root.append(elem)
    
    return tostring(root,encoding='UTF-8', method='xml', xml_declaration=True)

def get_places(result):
    plcs = {'places':[]}
    for row in result:
        plc = {
            row.name:{
                'id': (row.id),
                'coordinates':{
                    'latitude': (row.latitude),
                    'longitude': (row.longitude)
                }
            }
        }
        plcs['places'].append(plc)
    return plcs

def get_places_xml(result):
    root =Element('places')

    for row in result:
        elem = Element('place')
        elem.set('id',str(row.id))

        name = Element('name')
        coordinates = Element('coordinates')
        latitude = Element('latitude')
        longitude = Element('longitude')

        name.text = row.name
        latitude.text = str(row.latitude)
        longitude.text = str(row.longitude)
        
        coordinates.append(latitude)
        coordinates.append(longitude)

        elem.append(name)
        elem.append(coordinates)
        root.append(elem)
    
    return tostring(root,encoding='UTF-8', method='xml', xml_declaration=True)

def get_place_response(xml):
    tree = ET.fromstring(xml)
    place_dic={'place':{}}
    inner_dic = {}
    name = None
    for node in tree.iter('place'):
        for elem in node:
            if not elem.tag==node.tag:
                if elem:
                    inner_dic[name][elem.tag] = recursive(elem)
                else:
                    if elem.tag == 'name':
                        name = elem.text
                        inner_dic = {elem.text :{}}
                    inner_dic[name][elem.tag] = elem.text
    place_dic['place'].update(inner_dic)
    return place_dic

def recursive(list):
    if list:
        rec_dic={}
        for elem in list:
            rec_dic[elem.tag] = recursive(elem)
        return rec_dic
    else:
        return list.text

#ROUTE BUILDER
def get_routes(result):
    rts = {'routes':[]}
    for row in result:
        rt = {
            row.name:{
                'id': (row.id),
                'locations':{
                    'start_id': (row.start_id),
                    'end_id': (row.end_id)
                },
                'user_id': row.user_id
            }
        }
        rts['routes'].append(rt)
    return rts

def get_routes_xml(result):
    root =Element('routes')

    for row in result:
        elem = Element('route')
        elem.set('id',str(row.id))

        name = Element('name')
        locations = Element('locations')
        start = Element('start_id')
        end = Element('end_id')
        user_id = Element('user_id')

        name.text = row.name
        start.text = str(row.start_id)
        end.text = str(row.end_id)
        user_id.text = str(row.user_id)
        
        locations.append(start)
        locations.append(end)

        elem.append(name)
        elem.append(locations)
        elem.append(user_id)
        root.append(elem)
    
    return tostring(root,encoding='UTF-8', method='xml', xml_declaration=True)

def get_route(row):
    rts = {'routes':[]}
    rt = {
        row.name:{
            'id': (row.id),
            'locations':{
                'start_id': (row.start_id),
                'end_id': (row.end_id)
            },
            'user_id': row.user_id
        }
    }
    rts['routes'].append(rt)
    return rts

def get_route_xml(row):
    root =Element('routes')

    elem = Element('route')
    elem.set('id',str(row.id))

    name = Element('name')
    locations = Element('locations')
    start = Element('start_id')
    end = Element('end_id')
    user_id = Element('user_id')

    name.text = row.name
    start.text = str(row.start_id)
    end.text = str(row.end_id)
    user_id.text = str(row.user_id)
        
    locations.append(start)
    locations.append(end)

    elem.append(name)
    elem.append(locations)
    elem.append(user_id)
    root.append(elem)
    
    return tostring(root,encoding='UTF-8', method='xml', xml_declaration=True)

def get_route_response(xml):
    tree = ET.fromstring(xml)
    place_dic={'route':{}}
    for node in tree.iter('route'):
        for elem in node:
            if not elem.tag==node.tag:
                if elem:
                    place_dic['route'][elem.tag] = recursive(elem)
                else:
                    place_dic['route'][elem.tag] = elem.text
    return place_dic

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
