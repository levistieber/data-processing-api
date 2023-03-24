from database import db

class User(db.Model):
    __tablename__ = 'user'
    __column_names__={'id','email','password','name','routes'}
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    routes = db.relationship('Route',lazy=True)

class Place(db.Model):
    __tablename__ = 'place'
    __column_names__={'id','name','latitude','longitude'}
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    name = db.Column(db.String(1000), unique=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

class Route(db.Model):
    __tablename__ = 'route'
    __column_names__={'id','name', 'start_id','end_id','user_id'}
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    name=db.Column(db.String(1000), unique=True)
    start_id = db.Column(db.Integer, db.ForeignKey('place.id'), nullable=False)
    end_id = db.Column(db.Integer, db.ForeignKey('place.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start = db.relationship('Place', foreign_keys=[start_id])
    end = db.relationship('Place', foreign_keys=[end_id])