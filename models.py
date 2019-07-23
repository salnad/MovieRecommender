from google.appengine.ext import ndb

class User(ndb.Model):
    first_name = ndb.IntegerProperty()
    last_name = ndb.IntegerProperty()
    email = ndb.StringProperty()
