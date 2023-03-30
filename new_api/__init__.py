from flask import Flask
from auth import auth_blueprint
from place import place_blueprint
from routes import route_blueprint
from database import db

# init SQLAlchemy so we can use it later in our models


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
with app.app_context():
    db.init_app(app)
    db.create_all()

app.register_blueprint(auth_blueprint)
app.register_blueprint(place_blueprint)
app.register_blueprint(route_blueprint)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
