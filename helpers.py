from models import *

def update_upcoming_status(data):
    shows = data.shows
    for i in range(len(shows)): #grabbing the single show to work with storstart_time=shows[i].start_time 
      start_time=shows[i].start_time
      today = datetime.today() 
      print(today)
      show = shows[i].id
      if start_time < today:
        print('past') #upcoming_status should be set to false
        event = Show.query.get(show)
        event.upcoming_status = False
        db.session.add(event)
        db.session.commit()
      elif start_time > today:    
        print('future') #upcoming_status True
        event = Show.query.get(show)
        event.upcoming_status = True
        db.session.add(event)
        db.session.commit()
      else: 
        print('present') #upcoming_status True
        event = Show.query.get(show)
        event.upcoming_status = True
        db.session.add(event)
        db.session.commit()

def upcoming_shows_count():
  venues = Venue.query.all()
  for venue in venues:
    shows = []

    for i in range(len(venue.shows)):
      shows.append(venue.shows[i].upcoming_status)

    venue_to_edit= Venue.query.get(venue.id)
    venue_to_edit.upcoming_shows_count = shows.count(True)
    venue_to_edit.past_shows_count = shows.count(False)
    db.session.add(venue_to_edit)
    db.session.commit()
