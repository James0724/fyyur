from email.policy import default
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import logging
from flask_migrate import Migrate
from logging import FileHandler, Formatter
from flask_migrate import Migrate
from forms import *


#Configs
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)

#Venue database Models
class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120), nullable=False)
    seeking_talent = db.Column(db.Boolean)
    website_link = db.Column(db.String(200), nullable=False)
    seeking_description = db.Column(db.String(300))
    shows = db.relationship('Show', backref='venue', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    upcoming_shows_count = db.Column(db.Integer,)
    past_shows_count = db.Column(db.Integer,)
    db.UniqueConstraint(name)

    def __repr__(self):
      return f'<Venue {self.name}>'
        

#Artist database model  

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120), nullable=False)
    seeking_venue = db.Column(db.Boolean)
    website_link = db.Column(db.String(200), nullable=False)
    seeking_description = db.Column(db.String(300))
    shows = db.relationship('Show', backref='artist', lazy=True)
    available = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    upcoming_shows_count = db.Column(db.Integer,)
    past_shows_count = db.Column(db.Integer,)
    db.UniqueConstraint(name)

    def __repr__(self):
      return f'<Artist {self.name}>'

#Shows db model 

class Show(db.Model):
  __tablename__='Shows'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  start_time = db.Column(db.DateTime, nullable=False)
  upcoming_status =db.Column(db.Boolean, default=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  
  
  def __repr__(self):
      return f'<Show {self.name}, {self.venue.name}, {self.artist.name}>'

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


#Launch
#----------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run()