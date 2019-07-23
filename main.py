#main.py
#the import section
import webapp2
import jinja2
import os
from models import User

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
            logout_url = users.create_logout_url('/')
            logout_button= '<a href="%s"> Log out</a>' % logout_url

            existing_user = User.query().filter(User. email == email_adress).get()
            if existing_user:
                self.response.write('Welcome Back ! ' + existing_user.first_name + "<br>" + logout_button)
            else:
                self.response.write('''Please register! "
                    <form method='post' action='/'>
                        Name: <input type='text' name='first name' + 'last name'>
                        <input type='submit'>
                    </form>
                    <br>
                    %s
                ''' % logout_button)

        else:
            login_url = users.create_login_url('/')
            login_button = '<a href="%s"> Sign In</a>' % login_url
            self.response.write("Please log into your account!<br>" + login_button)
def post(self):
    user = users.get_current_user()
    if user:
        cssi_user = CssiUser(
            first_name=self.request.get('first_name'),
            last_name=self.request.get('last_name'),
            email_adress=user.nickname()
        )

        cssi_user.put()
        self.response.write('Thank you for registering an account <a href="/">Home</a>')

#the app configuration section
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/', LoginHandler)
     #this maps the root url to the MainPage Handler
], debug=True)
