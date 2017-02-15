#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import jinja2
import os

from google.appengine.ext import db

# set up jinja
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),\
                               autoescape=True)

# Create a database (table) called Blog ...
class Blog(db.Model):
    title=db.StringProperty(required=True)
    blog=db.TextProperty(required=True)
    created=db.DateTimeProperty(auto_now_add=True)

class BaseHandler(webapp2.RequestHandler):
    """ Base RequestHandler class for the app.
        The other handlers inherit from this one.
    """
    def renderError(self,error_code,msg):
        """ Sends HTTP error code and error detail supplied by the app """
        self.error(error_code)
        self.response.write(msg)

class RootHandler(BaseHandler):
#class MainHandler(Handler):
    """ Handles requests coming in to '/'  """

    def get(self):
        title=""
        blog=""
        error=""
        # Create an instance for retrieving from the database ...
        blogs=db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC")
        #t = jinja_env.get_template("base.html")
        t = jinja_env.get_template("front-page.html")

        content=t.render(blogs=blogs)

        self.response.write(content)

    def post(self):
        title=self.request.get("title")
        blog=self.request.get("blog")

        if title and blog:
            #self.response.write("thanks")


            a=Blog(title=title,blog=blog) # Create an instance of Blog ...
            a.put()

            self.redirect("/")
        else:
            incomplete_err = "we need both a title and some blog contents!"

            t = jinja_env.get_template("base.html")

            content = t.render(title=title,blog=blog,error=incomplete_err)
            self.response.write(content)

class ListBlogs(BaseHandler):
    """ Handles requests coming in to /list """

    def get(self):
        blogs=db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC LIMIT 5")
        #t = jinja_env.get_template("base.html")
        t = jinja_env.get_template("list.html")

        content=t.render(blogs=blogs)

        self.response.write(content)
        #self.response.write("Control passed to /list")
    def post(self):
        # Add the blog.key().id() here ...
        #self.response.write("Setting up the 'a' object ...")
        #a=db.GqlQuery("SELECT * FROM Blog WHERE title=title")
        k=blog.key(a).id()
        if not k:
            self.response.write("Object k was not established")
        else:
            self.response.write("Object k was established")
            #self.redirect("/blog/"+str(int(k)))
            #self.response.write("Control passed to /list")

class AddBlogs(BaseHandler):
    def get(self):
        t = jinja_env.get_template("post-new.html")

        content=t.render()

        self.response.write(content)
        #self.response.write("Control passed to /add")

    def post(self):
        title=self.request.get("title")
        blog=self.request.get("blog")

        if title and blog:
            #self.response.write("thanks")
            good_msg="Your blog has been added to the database."

            a=Blog(title=title,blog=blog) # Create an instance of Blog ...
            a.put()
            # Add the blog.key().id() here ...
            k=Blog.key(a).id()
            if not k:
                self.response.write("Object k was not established")
            else:
                #self.response.write("Object k was established")
                self.redirect("/blog/"+str(int(k)))
        else:
            incomplete_err = "we need both a title and some blog contents!"

            t = jinja_env.get_template("post-new.html")

            content = t.render(title=title,blog=blog,error=incomplete_err)
            self.response.write(content)


        #self.response.write("Control passed to /add")

#class ViewPostHandler(webapp2.RequestHandler):
class ViewBlog(BaseHandler):
    def get(self, id):
        #pass #replace this with some code to handle the request
        #instance=Blog.get_by_id(int('5770237022568448'),Parent=None)
        rec=Blog.get_by_id(int(id))
        if rec:
            t = jinja_env.get_template('blog-detail.html')
            content=t.render(blog=rec)
            self.response.write(content)
        else:
            self.renderError(404,"Record Not Found !")

app = webapp2.WSGIApplication([
    ('/', RootHandler),
    ('/list', ListBlogs),
    ('/add', AddBlogs),
    webapp2.Route('/blog/<id:\d+>', ViewBlog)
    ], debug=True)
