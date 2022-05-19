#Imports 
import dateutil.parser
import babel
from flask import flash, redirect, render_template, request, url_for
from forms import *
from models import *

# Models
#----------------------------------------------------------------------------------------------------------------
# Moved to models.py | separations of concerns


# Filters.
#----------------------------------------------------------------------------------------------------------------
def format_datetime(value, format='medium'):
  if isinstance(value, str):
    date = dateutil.parser.parse(value)
  else:
        date = value
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

# Controllers
#----------------------------------------------------------------------------------------------------------------
@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#----------------------------------------------------------------------------------------------------------------

# Get All Venue 
@app.route('/venues/', methods=['GET'])
def venues():
  #num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
    return render_template('pages/venues.html', areas=Venue.query.all());

# Show Venue Details
@app.route('/venues/<int:venue_id>', methods=['GET'])
def show_venue(venue_id):
  data = Venue.query.get(venue_id)
  if data == None:
    return render_template('errors/404.html')
  return render_template('pages/show_venue.html', venue=data)

# Search Venue
@app.route('/venues/search/', methods=['POST'])
def search_venues():
  search = request.form.get('search_term')
  results = Venue.query.filter(Venue.name.ilike('%'+search+'%')).all()
  return render_template('pages/search_artists.html', search=search, results=results )

# Create Venue
@app.route('/venues/create', methods=['GET'])#dispay the venueForm to the user
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])#insert data to the data base
def create_venue_submission():

    try:  
        form = VenueForm(request.form)
        form_venue = Venue()
        form.populate_obj(form_venue)
        db.session.add(form_venue)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
        return redirect(url_for('venues'))

    except:
        db.session.rollback()
        flash('Venue ' + request.form['name'] + ' was not successfully listed!')
        return redirect(url_for('venues'))

    finally:
       db.session.close()

# Update Venue
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue_detail(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  if venue == None:
    return render_template('errors/404.html')
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):

  try:  
      venue = Venue.query.get(venue_id)
      form = VenueForm(request.form)
      form.populate_obj(venue)
      db.session.add(venue)
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully edited!')
      return redirect(url_for('show_venue_detail', venue_id=venue_id))
      
  except:
        db.session.rollback()
        flash('Venue ' + request.form['name'] + ' was not successfully listed!')
        return redirect(url_for('show_venue_detail', venue_id=venue_id))

  finally:
       db.session.close()

# Delete Venue
@app.route('/venues/<venue_id>/delete', methods=['GET'])
# I used 'DELETE' method here and it did not work, I was geting method
# not allowed so insted I circumvented this problem by useing 'GET' and 
# implemeneted a delete function on the db.session which solved the issue

def delete_venue(venue_id):
  data = Venue.query.filter(Venue.id == venue_id).first()
  try:
    if data != None:
      db.session.delete(data)
      db.session.commit()
      flash('Venue was successfully deleted!')
      return redirect(url_for('index'))
      
  except: #Handle cases where the session commit could fail.
    if data == None:
      print('Venue was not found!')
      return redirect(url_for('venues'))

#  Artists
#----------------------------------------------------------------------------------------------------------------

# Get all artists
@app.route('/artists/')
def artists():
  return render_template('pages/artists.html', artists=Artist.query.all());

# Search Artist
@app.route('/artists/search/', methods=['POST'])
def search_artists():
  search = request.form.get('search_term')
  results = Artist.query.filter(Artist.name.ilike('%'+search+'%')).all()
  return render_template('pages/search_artists.html', search=search, results=results )

# Show Artist Details
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  data = Artist.query.get(artist_id)
  if data == None:
    return render_template('errors/404.html')
  return render_template('pages/show_artist.html', artist=data)


# Create Artist
@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  try:
    form = ArtistForm(request.form)
    artist = Artist()
    form.populate_obj(artist)
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    return redirect(url_for('artists'))

  except Exception as e:
    db.session.rollback()
    flash('Artist was not succesfully added!')
    print(str(repr(e)))
    return redirect(url_for('artists'))

  finally:
    db.session.close()

# Update Artist 
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  if artist == None:
    return render_template('errors/404.html')
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

  try:
    artist = Artist.query.get(artist_id)
    form = ArtistForm(request.form)
    form.populate_obj(artist)
    db.session.add(artist)
    db.session.commit()
  except:
    db.session.rollback()
  
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

# Delete Artist
@app.route('/artists/<artist_id>/delete', methods=['GET'])
def delete_artist(artist_id):
  try:  
      data = Artist.query.filter(Artist.id == artist_id).first()
      db.session.delete(data)
      db.session.commit()
      flash('Artist was successfully deleted!')
      return redirect(url_for('artists'))
      
  except: 
        db.session.rollback()
        flash('Artist was not successfully deleted!')
        return redirect(url_for('artists'))

  finally:
       db.session.close()

#  Shows
#----------------------------------------------------------------------------------------------------------------

# Get all show
@app.route('/shows')
def shows():
  return render_template('pages/shows.html', shows=Show.query.all())

# Search Show
@app.route('/shows/search/', methods=['POST'])
def search_show():
  search = request.form.get('search_term')
  results = Show.query.filter(Show.name.ilike('%'+search+'%')).all()
  return render_template('pages/search_shows.html', search=search, results=results )

# Create show
@app.route('/shows/create', methods=['GET'])
def create_shows():
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_shows_submission():
  form = ShowForm(request.form)
  show = Show()
  form.populate_obj(show)
  artist_id = request.form['artist_id']
  artist_avaibality = Artist.query.get(artist_id).available

  try:   
    if artist_avaibality == True:
      db.session.add(show)
      db.session.commit()
      flash(request.form['name'] + ' was successfuly added!')
    else:
      flash(request.form['name'] + ' was not successfuly added artist is unavailable or fully booked!')
      return render_template('forms/new_show.html', form=form)
    return redirect(url_for('shows'))

  except:
    if artist_avaibality == False:
      flash(request.form['name'] + ' was not successfuly added! artist is unavailable')
    db.session.rollback()
    return render_template('forms/new_show.html', form=form)
  finally:
    db.session.close()
    
# Show Details
@app.route('/shows/<int:show_id>')
def show_details(show_id):
  data = Show.query.get(show_id)
  if data == None:
    return render_template('errors/404.html')
  return render_template('pages/show_details.html', show=data)

#Error Handler
#----------------------------------------------------------------------------------------------------------------

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500




