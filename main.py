import webapp2
import re
import cgi

signup_form = """
<!DOCTYPE html>
<html>
<head>
    <title>Assignment 3: Formation-Signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>Signup</h1>
        <form method="post">
            <div>
                <label for="username">Username&emsp;&emsp;&ensp;</label>
                <input type="text" name="username" value="%(username)s">
                <label style="color: red">%(error_u)s</label>
            </div>
            <br>
            <div>
                <label for="password">Password&emsp;&emsp;&ensp;&nbsp;</label>
                <input type="password" name="password" value="">
                <label style="color: red">%(error_p)s</label>
            </div>
            <br>
            <div>
                <label for="verify">Verify Password</label>
                <input type="password" name="verify" value="">
                <label style="color: red">%(error_v)s</label>
            </div>
            <br>
            <div>
                <label for="email">Email (optional)</label>
                <input type="text" name="email" value="%(email)s">
                <label style="color: red">%(error_e)s</label>
            </div>
            <br>
            <input type="submit">
        </form>
</body>
</html>
"""

welcome_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Assignment 3: Formation-Signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
"""

welcome_footer = """
</body>
</html>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Signup(webapp2.RequestHandler):
    def write_form(self, error_u="", error_p="", error_v="", error_e="", username="", email=""):
        self.response.out.write(signup_form % {"error_u": error_u,
                                               "error_p": error_p,
                                               "error_v": error_v,
                                               "error_e": error_e,
                                               "username": username,
                                               "email": email})

    def get(self):
        self.write_form()

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        error_u = self.request.get('error_u')
        error_p = self.request.get('error_p')
        error_v = self.request.get('error_v')
        error_e = self.request.get('error_e')

        params = dict(username = username,
                      email = email,
                      error_u = error_u,
                      error_p = error_p,
                      error_v = error_v,
                      error_e = error_e,)

        if not valid_username(username):
            error_u = "For shame, that's not a valid username!"
            error_element_u = cgi.escape(error_u, quote=True)
            have_error = True
#            self.redirect('/?error=' + error)

        if not valid_password(password):
            error_p = "Your password is awful, and you are awful!"
            error_element_p = cgi.escape(error_p, quote=True)
            have_error = True
#            self.redirect('/?error=' + error)
        elif password != verify:
            error_v = "Really? I won't swipe right until you prove you can match!"
            error_element_v = cgi.escape(error_v, quote=True)
            have_error = True
#            self.redirect('/?error=' + error)

        if not valid_email(email):
            error_e = "What, are you bashful? I may want to get in touch!"
            error_element_e = cgi.escape(error_e, quote=True)
            have_error = True
#            self.redirect('/?error=' + error)

        if have_error:
            self.write_form(error_u, error_p, error_v, error_e, username, email)
        else:
            self.redirect('/welcome?username=' + username)


class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        welcome_user = "<h1><strong>Welcome, " + username + "!</strong></h1>"
        response = welcome_header + welcome_user + welcome_footer
        if valid_username(username):
            self.response.write(response)
        else:
            self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', Signup),
    ('/welcome', Welcome)
], debug=True)
