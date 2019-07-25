from google.appengine.ext import ndb

class Movie(ndb.Model):
    title = ndb.StringProperty(required=True)
    plot = ndb.StringProperty(required=True)
    poster = ndb.StringProperty(required=True)
    id = ndb.IntegerProperty(required=True)

class User(ndb.Model):
    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    favorite_movies = ndb.IntegerProperty(repeated=True)
