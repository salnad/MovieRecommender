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

class DataPage(webapp2.RequestHandler):
    def post(self):
        movie_title = self.request.get('Title: ')
        movie_plot = self.request.get('Plot: ')
        movie_director = self.request.get('Director: ')
        }
        #create movie object
        movie_info = Movie(
            title = movie_title,
            plot = movie_plot,
            director = movie_director
        )
        #store it in data store
        movie_info.put()

        result_template = jinja_env.get_template('results.html')
        self.response.write(result_template.render(data_dict))

#the app configuration section
app = webapp2.WSGIApplication([
    ('/', MainPage), #this maps the root url to the MainPage Handler
], debug=True)
