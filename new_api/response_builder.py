import re
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, tostring

def credentials(xml):
    tree = ET.fromstring(xml)
    cred_dic={'credentials':{}}
    for node in tree.iter('credentials'):
        for elem in node.iter():
            if not elem.tag==node.tag:
                cred_dic['credentials'][elem.tag] = elem.text
    return cred_dic

def get_place(result):
    plcs = {'places':{}}
    plc = {
        result.name:{
            'id': (result.id),
            'coordinates':{
                'latitude': (result.latitude),
                'longitude': (result.longitude)
            }
        }
    }
    plcs['places'].update(plc)
    return plcs

def get_places(result):
    plcs = {'places':{}}
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
        plcs['places'].update(plc)
    return plcs

def get_place_xml(result):
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
    
    return tostring(root,encoding='UTF-8', method='xml')