from flask import Flask
from auth import auth_blueprint
from place import place_blueprint
from routes import route_blueprint
from error_handlers import *
from database import db

app = Flask(__name__)

app.config['TRAP_HTTP_EXCEPTIONS']=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
with app.app_context():
    db.init_app(app)
    db.create_all()

app.register_blueprint(auth_blueprint)
app.register_blueprint(place_blueprint)
app.register_blueprint(route_blueprint)
app.register_error_handler(500, not_allowed)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
