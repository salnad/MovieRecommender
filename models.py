from google.appengine.ext import ndb

<<<<<<< HEAD
class User(ndb.Model):
    first_name = ndb.IntegerProperty()
    last_name = ndb.IntegerProperty()
    email = ndb.StringProperty()
=======
class Movie(ndb.Model):
    title = ndb.StringProperty(required=True)
    plot = ndb.StringProperty(required=True)
    director = ndb.StringProperty(required=True)
>>>>>>> e510714c7836c7b0c63a70837e8068bc5743c36b
