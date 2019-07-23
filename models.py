from google.appengine.ext import ndb

class Movie(ndb.Model):
    title = ndb.StringProperty(required=True)
    plot = ndb.StringProperty(required=True)
    director = ndb.StringProperty(required=True)
