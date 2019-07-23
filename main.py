#main.py
#the import section
import webapp2
import jinja2
from models import User
from models import Movie
import os, json
from google.appengine.api import users
from google.appengine.api import urlfetch

api_key = "3f44093c7132e8d90dfece35961ffafa"

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

#the handler section
class MainPage(webapp2.RequestHandler):
    def get(self): #for a GET request
        self.response.write('Hello, World!') #the responseclass LoginHandler(webapp2.RequestHandler):

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            email_address = user.nickname()
            logout_url = users.create_logout_url('/login')
            logout_button= '<a href="%s"> Log out</a>' % logout_url

            existing_user = User.query().filter(User.email == email_address).get()
            if existing_user:
                self.response.write('Welcome Back, ' + existing_user.first_name + "<br>" + logout_button)
            else:
                self.response.write('''Please register!
                    <form method='post' action='login'>
                        First Name: <input type='text' name='first_name'>
                        Last Name: <input type='text' name='last_name'>
                        <input type='submit'>
                    </form>
                    <br>
                    %s
                ''' % logout_button)

        else:
            login_url = users.create_login_url('/login')
            login_button = '<a href="%s"> Sign In</a>' % login_url
            self.response.write("Please log into your account!<br>" + login_button)
    def post(self):
        user = users.get_current_user()
        if user:
            cssi_user = User(
                first_name=self.request.get('first_name'),
                last_name=self.request.get('last_name'),
                email=user.nickname()
            )

            cssi_user.put()
            self.response.write('Thank you for registering an account <a href="/">Home</a>')

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
        search_term = search_term.replace(' ', '+')
        # generate a api_url based upon that search term
        api_url = "https://api.themoviedb.org/3/search/movie?api_key=" + api_key + "&query=" + search_term
        # get the json result for search using urlfetch api call
        loaded_json_data = urlfetch.fetch(api_url).content
        loaded_response = json.loads(loaded_json_data)
        # empty loaded_movies array (initialize it)
        loaded_movies = loaded_response['results']

        # data to be put onto webpage 'search_term' (term user searched), and 'searched_movies' (movies returned from that term)

        search_data = {
            "search_term" : search_term,
            "searched_movies" : loaded_movies
        }
        # load search_template using jinja, and rendering it onto the webpage
        search_template = jinja_env.get_template('templates/search.html')
        self.response.write(search_template.render(search_data))

class DataPage(webapp2.RequestHandler):
    def get(self):
        movie_title = self.request.get('Title: ')
        movie_plot = self.request.get('Plot: ')
        movie_director = self.request.get('Director: ')

        #create movie object
        movie_info = Movie(
            title = movie_title,
            plot = movie_plot,
            director = movie_director
        )
        #store it in data store
        movie_info.put()



#the app configuration section
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/login', LoginHandler),
    ('/data', DataPage),
     #this maps the root url to the MainPage Handler
    ('/search', SearchPage) #this maps the root url to the MainPage Handler
], debug=True)
