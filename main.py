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
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return not email or EMAIL_RE.match(email)


form = """<form method = "post">
        <h2> User Signup</h2>
        <br>
        <label>Username:
        <input type='text' name='username' value = '%(username)s'></label>
        <label> %(error_username)s </label>
        <br>
        <br>
        <label> Password
        <input type = 'password' name='password' value = ''> </label>
        <label> %(error_password)s </label>
        <br>
        <br>
        <label>Verify Password:
        <input type = 'password' name='verify' value = ''> </label>
        <label> %(error_verify)s </label>
        <br>
        <br>
        <label> Email
        <input type ='text' name='email' value = '%(email)s'></label>
        <label> %(error_email)s </label>
        <br>
        <br>
        <input type = 'submit'/>"""


class MainHandler(webapp2.RequestHandler):
    def write_form(self, email="", username = "", error_username = "",error_password = "",error_verify = "",error_email = ""):
        self.response.out.write(form % {"email": email,
                                        "username": username,
                                        "error_username":error_username,
                                        "error_password": error_password,
                                        "error_verify": error_verify,
                                        "error_email": error_email})

    def get(self):
        self.write_form( )

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify_password = self.request.get("verify")
        email = self.request.get("email")
        have_errors = False
        error_username = ""
        error_password = ""
        error_verify = ""
        error_email = ""

        if not valid_username(username):
            error_username = "You need to enter a valid username."
            have_errors = True

        if not valid_password(password):
            error_password = "You need to enter a valid password."
            have_errors = True

        elif password != verify_password:
            error_verify = "Your passwords do not match."
            have_errors = True

        if not valid_email(email):
            error_email = "Your email is not valid."
            have_errors = True

        if have_errors:
            paramers = "You didn't type anything!"
            self.write_form(email, username, error_username,error_password,error_verify,error_email)
        else:
            self.redirect("/welcome?username=" + username)

class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        if valid_username(username):
            self.response.write("<h1>" + "Welcome, " + username + "!"+"</h1>")
        else:
            self.redirect("/")



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)
