import webapp2
import cgi
import jinja2
import os
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

class Post(db.Model):
  title = db.StringProperty(required = True)
  content = db.TextProperty(required = True)
  created = db.DateTimeProperty(auto_now_add = True)

class Handler(webapp2.RequestHandler):
  
  def renderError(self, error_code):
      self.error(error_code)
      self.response.write('Nice job, you broke it. Try it again.')

class Index(Handler):
    def get(self):
      posts = db.GqlQuery('SELECT * FROM Post ORDER BY created DESC LIMIT 5')
        


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
