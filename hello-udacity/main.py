import os
import webapp2
import re
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
    def render(self,template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

class Rott13(BaseHandler):
    def get(self):
        self.render('rot13-form.html')

    def post(self):
        rot13 = ''
        text = self.request.get('text')
        if text:
            rot13 = text.encode('rot13')

        self.render('rot13-form.html', text = rot13)

form="""
<form method="post" action="/testform">
    <textarea name="text">
%s
    </textarea>
    <input type="submit">
</form>
"""

signupform="""
<form method="post" action="/hw2">
    name<input name="username" value="%(username)s">%(err_username)s<br>
    password<input type="password" name="password" value="%(password)s">%(err_password)s<br>
    verify password<input type="password" name="verify" value="%(verify)s">%(err_verify)s<br>
    email<input type="email" name="email" value="%(email)s">%(err_email)s<br>
    <input type="submit">
</form>
"""

def sentence_rot13(str):
    result = "";
    for i in range(0, len(str)):
        result += rot13(str[i])
    print result;
    return result;

def rot13(char):
    asc = ord(char)
    char_a = ord("a")
    char_m = ord("m")
    char_ca = ord("A")
    char_cm = ord("M")
    char_z = ord("z")
    char_cz = ord("Z")

    if asc >= char_a and asc <= char_m:
        asc += 13
    elif asc > char_m and asc <= char_z:
        asc -= 13
    elif asc >= char_ca and asc <= char_cm:
        asc += 13
    elif asc > char_cm and asc <= char_cz:
        asc -= 13

    return chr(asc)


USERNAME_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")




def valid_username(username):
    return USERNAME_RE.match(username)


def valid_password(str):
    return PASSWORD_RE.match(str)

def valid_email(str):
    if len(str) > 0:
        return EMAIL_RE.match(str)
    else:
        return True


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(form % "")


class SignUpPage(webapp2.RequestHandler):
    def get(self):
        err_msg = {"username":"", "err_username": "", "password":"", "err_password": "", "verify": "", "err_verify": "", "email": "", "err_email": ""}
        self.response.out.write(signupform % err_msg)

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        err_msg = {"username":username, "err_username": "", "password":password, "err_password": "", "verify": verify, "err_verify": "", "email": email, "err_email": ""}

        valid = True

        if not valid_username(username):
            valid = False
            err_msg["err_username"] = "That's not a valid user name."

        if not valid_password(password):
            valid = False
            err_msg["err_password"] = "That wasn't a valid password."

        elif password != verify:
            valid = False
            err_msg["err_verify"] = "Your passwords didn't match."

        if not valid_email(email):
            valid = False
            err_msg["err_email"] = "That's not a valid email."

        if valid:
            self.redirect("/hw2/welcome?username=" + username )


        else:
            self.response.out.write(signupform % err_msg)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")

        self.response.out.write("Welcome, ")
        self.response.out.write(username)

class TestHandler(webapp2.RequestHandler):
    def post(self):
        text = self.request.get("text")
        #self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(form % sentence_rot13(text))
        #self.response.out.write(self.request);

config = {}
config['webapp2_extras.sessions'] = {'secret_key': 'some-secret-key-to-use',}
app = webapp2.WSGIApplication([('/', MainPage),
('/testform', TestHandler),
('/hw2', SignUpPage),
('/hw2/rot13', Rott13),
('/hw2/welcome', WelcomeHandler)]
, debug=True)
