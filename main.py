#main.py
#the import section
import webapp2
import jinja2
import os

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

#the handler section
class MainPage(webapp2.RequestHandler):
    def get(self): #for a GET request
        self.response.write('Hello, World!') #the response

#the app configuration section
app = webapp2.WSGIApplication([
    ('/', MainPage), #this maps the root url to the MainPage Handler
], debug=True)
