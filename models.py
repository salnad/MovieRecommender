from google.appengine.ext import ndb

class User(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()

class Movie(ndb.Model):
    title = ndb.StringProperty(required=True)
    plot = ndb.StringProperty(required=True)
    director = ndb.StringProperty(required=True)
