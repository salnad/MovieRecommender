#main.py
#the import section
import webapp2
import jinja2
import os, json
from google.appengine.api import urlfetch

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

#the handler section
class MainPage(webapp2.RequestHandler):
    def get(self): #for a GET request
        self.response.write('Hello, World!') #the response

class SearchPage(webapp2.RequestHandler):
    def get(self):
        # 'default text' of the search bar
        search_term = "John Wick..."
        # data to pass into search template, 'default text' and empty results array because user has not yet searched
        search_data = {
            "search_term" : search_term,
            "searched_movies" : []
        }
        # load jinja template using 'search.html' (gives a search bar to search, and puts all results in a unordered list)
        search_template = jinja_env.get_template('templates/search.html')
        # render and load the empty, search page
        self.response.write(search_template.render(search_data))



    def post(self):
        # get the search term from the form upon submission
        search_term = self.request.get('search_title')
        # replace spaces with underscores (otherwise, API cannot parse)
        search_term = search_title.replace(' ', '_')
        # generate a api_url based upon that search term
        api_url = "http://www.omdbapi.com/?apikey=ecca4fde&page=1&s=" + search_term
        # get the json result for search using urlfetch api call
        loaded_json_data = urlfetch.fetch(api_url).content
        # empty loaded_movies array (initialize it)
        loaded_movies = []
        # check if the loaded data is in the form of a dictionary
        if loaded_json_data[0] == '{':
            # convert json data into a dictionary
            loaded_response = json.loads(loaded_json_data)
            # check if the search resulted has properly been processed
            if loaded_response['Response'] != 'False':
                # set the results (list of movies) for the search terms as loaded_movies
                loaded_movies = loaded_response['Search']

        # data to be put onto webpage 'search_term' (term user searched), and 'searched_movies' (movies returned from that term)
        search_data = {
            "search_term" : search_title,
            "searched_movies" : loaded_movies
        }
        # load search_template using jinja, and rendering it onto the webpage
        search_template = jinja_env.get_template('templates/search.html')
        self.response.write(search_template.render(search_data))

#the app configuration section
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/search', SearchPage) #this maps the root url to the MainPage Handler
], debug=True)
