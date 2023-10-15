from flask import Flask
from auth import auth_blueprint
from place import place_blueprint
from routes import route_blueprint
from error_handlers import *
from database import db

def create_app():
    #App creation. __name__ is the current Python module
    app = Flask(__name__)

    #App configuration
    app.config['TRAP_HTTP_EXCEPTIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #Database creation
    with app.app_context():
        db.init_app(app)
        db.create_all()

    #Registering blueprints
    blueprints = [auth_blueprint, place_blueprint, route_blueprint]
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    #Registering error handler(s)
    app.register_error_handler(500, not_allowed)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
