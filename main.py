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
      
      t = jinja_env.get_template("mainpage.html")
      content = t.render(posts = posts)
      self.response.write(content)
    
    
      

class NewPost(Handler):
  def get(self):
    error = ""
    t = jinja_env.get_template('newpost.html')
    content = t.render(error = error)
    self.response.write(content)
  
  def post(self):
    post_title = self.request.get('post-title')
    post_content = self.request.get('post-content')
    post_title_esc = cgi.escape(post_title)
    post_content_esc = cgi.escape(post_content)
    
    post = Post(title = post_title_esc, content = post_content_esc)
    post.put()
    
    t = jinja_env.get_template('post-confirmation.html')
    content = t.render()
    self.response.write(content)
    
    
app = webapp2.WSGIApplication([
    ('/', Index), ('/newpost', NewPost)
], debug=True)
