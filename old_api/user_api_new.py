from xml.dom.minidom import parseString
from xml.etree.ElementTree import Element,tostring
from flask import Response
from flask import request, jsonify
from toxml import *
from errors import *

from api_mysql import mysql

from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return 'Login'

@auth.route('/signup')
def signup():
    return 'Signup'

@auth.route('/logout')
def logout():
    return 'Logout'
