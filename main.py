#main.py
#the import section
from models import User, Movie
import os, json, webapp2, jinja2, random
from google.appengine.api import users, urlfetch
from google.appengine.ext import ndb

current_recommendations = []

api_key = "3f44093c7132e8d90dfece35961ffafa"
PARENT_KEY_FOR_USER = ndb.Key('Entity', 'user_root_key')

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def recommend_movies(movie_id):
    # generate a api_url based upon the movie_id
    loaded_movies = []
    api_url = 'https://api.themoviedb.org/3/movie/' + movie_id + '/recommendations?api_key=' + api_key + '&language=en-US&page=1'
    # get the json result for search using urlfetch api call
    loaded_json_data = urlfetch.fetch(api_url).content
    loaded_response = json.loads(loaded_json_data)
    # set list of movie to 'results' field
    if loaded_response.has_key('results'):
        loaded_movies = loaded_response['results']
    # return results
    return loaded_movies

def search_movies(search_term):
    search_term = search_term.replace(' ', '+')
    # generate a api_url based upon that search term
    api_url = "https://api.themoviedb.org/3/search/movie?api_key=" + api_key + "&query=" + search_term
    # get the json result for search using urlfetch api call
    loaded_json_data = urlfetch.fetch(api_url).content
    loaded_response = json.loads(loaded_json_data)
    # set list of movie to 'results' field
    loaded_movies = loaded_response['results']
    # return results
    return loaded_movies

def get_movie_from_id(movie_id):
    api_url = "https://api.themoviedb.org/3/movie/" + str(movie_id) + "?api_key=" + api_key
    loaded_json_data = urlfetch.fetch(api_url).content
    loaded_response = json.loads(loaded_json_data)
    return loaded_response

def get_recommendations(arr, sz):
    movie_dict = {}
    for movie in arr:
        if type(movie) == str:
            continue
        this_movies_recc = recommend_movies(str(movie['id']))
        for recc_movie in this_movies_recc:
            if recc_movie['id'] in movie_dict:
                movie_dict[recc_movie['id']] += 1
            else:
                movie_dict[recc_movie['id']] = 1
    temp = 0
    result = []
    for key, value in sorted(movie_dict.items(), key=lambda item: item[1], reverse = True):
        if temp == sz:
            break
        result.append(get_movie_from_id(key))
        temp += 1
    return result

def compare_movie_list(movie1, movie2):
    return len(set(movie1).intersection(movie2))

def streaming_sites(search_term):
    utelly_json_data = unirest.get("https://utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com/lookup?term=bojack&country=us".content,
    headers={
        "X-RapidAPI-Host": "utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com",
        "X-RapidAPI-Key": "f64badbe6amshfc501a81d7aec7bp184a75jsn6abbf636ff40"
      }
    )
    loaded_response = json.loads(utelly_json_data)
    loaded_streaming_sites = loaded_response['results']

    return loaded_streaming_sites

#the handler section
class MainPage(webapp2.RequestHandler):
    def get(self): #for a GET request
        user = users.get_current_user()
        registered_user = None
        # print(user.nickname())
        if not user:
            button_url = users.create_login_url('/login')
            is_logged_in = False
        else:
            button_url = users.create_logout_url('/')
            registered_user = User.query(ancestor=PARENT_KEY_FOR_USER).filter(User.email == user.nickname()).get()
            is_logged_in = True
        main_data = {
            "is_logged_in" : is_logged_in,
            "button_url": button_url,
            "user" : registered_user
        }

        main_template = jinja_env.get_template('templates/main.html')
        self.response.write(main_template.render(main_data))

class LoginHandler(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        existing_user = User.query(ancestor=PARENT_KEY_FOR_USER).filter(User.email == user.nickname()).get()
        if existing_user:
            self.redirect('/')
        else:
            register_template =jinja_env.get_template('templates/register.html')
            self.response.write(register_template.render())

    def post(self):
        new_user = User(
            parent=PARENT_KEY_FOR_USER,
            first_name=self.request.get('first_name'),
            last_name=self.request.get('last_name'),
            email = users.get_current_user().nickname(),
            favorite_movies = []
        )
        new_user.put()
        self.redirect('/')

class SearchPage(webapp2.RequestHandler):
    def get(self):
        # 'default text' of the search bar
        search_term = "John Wick..."
        # data to pass into search bar, 'default text' and empty results array because user has not yet searched
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
        # use search_movies to search using the API, and store it in loaded_movies
        loaded_movies = search_movies(search_term)

        # data to be put onto webpage 'search_term' (term user searched), and 'searched_movies' (movies returned from that term)
        search_data = {
            "search_term" : search_term,
            "searched_movies" : loaded_movies
        }
        # load search_template using jinja, and rendering it onto the webpage
        search_template = jinja_env.get_template('templates/search.html')
        self.response.write(search_template.render(search_data))

class RecommendedPage(webapp2.RequestHandler):
    def get(self):
        global current_recommendations

        search_term = "John Wick..."

        # data to pass into search bar, 'default text' and empty results array because user has not yet searched
        search_data = {
            "search_term" : search_term,
            "searched_movies" : []
        }
        # load jinja template using 'recommended.html' (gives a search bar to search, and puts all results in a unordered list)
        search_template = jinja_env.get_template('templates/recommendedplus.html')
        # render and load the empty, search bar on the recommended page
        self.response.write(search_template.render(search_data))


    def post(self):
        user_email = users.get_current_user().nickname()
        current_user = User.query(ancestor=PARENT_KEY_FOR_USER).filter(User.email == user_email).get()
        global current_recommendations
        current_recommendations = []
        recommended_movies = []
        search_term = ""

        current_form = self.request.get('form_name')

        if current_form == "SEARCHFORM":
            search_term = self.request.get('search_term')
            loaded_movies = search_movies(search_term)

            # check if loaded_movies isn't empty
            if len(loaded_movies) > 0:
                # get the most 'relevant movie' to the search
                seed_movie = loaded_movies[0]
                print(seed_movie)
                # get the id of the 'most relevant movie' for the seed of the recommendation
                seed_movie_id = seed_movie['id']
                # set recommended_movies to recommend movies based on the seed movie's id
                new_recommendations = recommend_movies(str(seed_movie_id))
                current_recommendations += new_recommendations
                recommended_movies = current_recommendations[0:10]

        elif current_form == "REFINEFORM":
            submit_button = self.request.get('submit')
            if submit_button:
                for i in range(10):
                    currel = self.request.get('mov' + str(i+1))
                    if currel != '':
                        current_user.favorite_movies += [int(currel)]
                current_user.put()
                self.redirect('/')
                return
            for i in range(10):
                currel = self.request.get('mov' + str(i+1))
                if currel != '':
                    current_recommendations += recommend_movies(str(currel)) + [get_movie_from_id(currel)]
            recommended_movies = get_recommendations(current_recommendations,10)

        # data to be put onto webpage 'search_term' (term user searched), and 'recommended_movies' (movies recommended for searched_term)
        recommended_data = {
            "search_term" : search_term,
            "recommended_movies" : recommended_movies
        }
        # load search_template using jinja, and rendering it onto the webpage
        recommended_template = jinja_env.get_template('templates/recommendedplus.html')
        self.response.write(recommended_template.render(recommended_data))

class SocialPage(webapp2.RequestHandler):
    def get(self):
        user_email = users.get_current_user().nickname()
        current_user = User.query(ancestor=PARENT_KEY_FOR_USER).filter(User.email == user_email).get()
        favorite_movies = current_user.favorite_movies
        favorite_movies = map(get_movie_from_id, favorite_movies)
        user_data = {
            "favorite_movies" : favorite_movies
        }
        user_template = jinja_env.get_template('templates/social.html')
        self.response.write(user_template.render(user_data))

    def post(self):
        user_email = users.get_current_user().nickname()
        current_user = User.query(ancestor=PARENT_KEY_FOR_USER).filter(User.email == user_email).get()
        all_users = User.query().fetch()
        list = []
        for user in all_users:
            list.append((user, compare_movie_list(user.favorite_movies, current_user.favorite_movies)))
        list = sorted(list, key = lambda x: x[1], reverse = True)[1:]
        self.response.write(list)

class DataPage(webapp2.RequestHandler):
    def get(self):
        user_email = users.get_current_user().nickname()
        current_user = User.query(ancestor=PARENT_KEY_FOR_USER).filter(User.email == user_email).get()
        list1 = [1,2,3,4,5,6]
        list2 = [3, 5, 7, 9]
        self.response.write(compare_movie_list(list1,list2))

        movie_title = self.request.get('Title: ')
        movie_plot = self.request.get('Plot: ')
        movie_director = self.request.get('Director: ')


class UserPage(webapp2.RequestHandler):
    def get(self):
        # 'default text' of the search bar
        search_term = "Netflix..."
        # data to pass into search bar, 'default text' and empty results array because user has not yet searched
        streaming_site_data = {
            "streaming_source" : streaming_source,
            "streaming_sites" : []
        }
        # load jinja template using 'user.html' (gives a search bar to search, and puts all results in a unordered list)
        streaming_template = jinja_env.get_template('templates/user.html')
        # render and load the empty, search page
        self.response.write(streaming_template.render(streamer_data))

    def post(self):
        # get the search term from the form upon submission
        search_term = self.request.get('search_term')

        loaded_sites =  streaming_sites(search_term)
        # use search_movies to search using the API, and store it in loaded_movies
        loaded_streaming_sites = []

        # data to be put onto webpage 'search_term' (term user searched), and 'searched_movies' (movies returned from that term)
        streamer_data = {
            "streaming_source" : streaming_source,
            "streaming_sites" : loaded_sites
        }

        # ===================== Put stuff on the screen =======================

        # load search_template using jinja, and rendering it onto the webpage
        streaming_template = jinja_env.get_template('templates/user.html')
        self.response.write(streaming_template.render(streamer_data))

#the app configuration section
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/login', LoginHandler),
    ('/data', DataPage),
    ('/recommended', RecommendedPage),
    ('/social', SocialPage),
    ('/search', SearchPage),
    ('/user', UserPage)
], debug=True)
