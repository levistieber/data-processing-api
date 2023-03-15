import flask
from api_fav_route import api_fav_route
from api_places import api_places
from api_users import api_users
from adminapi import adminapi
from error_handlers import *
from api_mysql import mysql

app = flask.Flask(__name__)

app.config['TRAP_HTTP_EXCEPTIONS']=True
app.register_error_handler(500, not_allowed)

app.register_blueprint(api_fav_route)
app.register_blueprint(api_places)
app.register_blueprint(api_users)
app.register_blueprint(error_handlers)
app.register_blueprint(adminapi)

app.config["DEBUG"] = False
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'egrip'

mysql.init_app(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
