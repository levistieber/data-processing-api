# Validate JSON response
# Returns False if error list was empty, meaning validation was successful
# Returns True if error lsit is not empty, meaning there were errors while validating the data
import json
from jsonschema import Draft7Validator
from lxml import etree


def validateJsonResponse(schemaLocation, dataReceived):
    # Validate schema
    with open(schemaLocation) as schemaFile:
        schema = json.load(schemaFile)
    schemaFile.close()

    validator = Draft7Validator(schema)

    listOfValidationErrors = list(validator.iter_errors(dataReceived))

    if (bool(listOfValidationErrors)):
        print("There were errors while validating the data!")
    else:
        print("Validated successfuly!")

    print("Errors while validating json:", listOfValidationErrors)

    return bool(listOfValidationErrors)


# Validate XML reponse using XSD
def validateXmlResponse(schemaLocation, xmlToValidate):
    #Create schema from string
    xmlschema_doc = etree.parse(schemaLocation)
    xmlschema = etree.XMLSchema(xmlschema_doc)

    xml_doc = etree.fromstring(xmlToValidate)
    result = xmlschema.validate(xml_doc)

    print("Errors while validating xml:", xmlschema.error_log)
    
    return result