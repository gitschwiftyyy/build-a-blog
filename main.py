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
  date = db.DateProperty(auto_now_add = True)

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
    error = cgi.escape(error)
    t = jinja_env.get_template('newpost.html')
    content = t.render(error = error)
    self.response.write(content)
  
  def post(self):
    post_title = self.request.get('post-title')
    post_content = self.request.get('post-content')
    post_title_esc = cgi.escape(post_title, quote=True)
    post_content_esc = cgi.escape(post_content, quote=True)
    
    if not post_title_esc or post_content_esc:
      error = "Please enter a title and content"
      t = jinja_env.get_template('newpost.html')
      content = t.render(error = cgi.escape(error))
      self.response.write(content)
    
    if post_title_esc and post_content_esc:
      post = Post(title = post_title_esc, content = post_content_esc)
      post.put()
      post_id = post.key().id()
      
      self.redirect('/blog/' + str(post_id))
      
    
class ViewPost(Handler):
    def get(self, id):
      post = Post.get_by_id(int(id))
      t = jinja_env.get_template('post.html')
      content = t.render(post = post)
      self.response.write(content)

class Redirect(Handler):
  def get(self):
    self.redirect('/blog')


app = webapp2.WSGIApplication([
    ('/blog', Index), ('/blog/newpost', NewPost), webapp2.Route('/blog/<id:\d+>', ViewPost), ('/', Redirect)
], debug=True)
