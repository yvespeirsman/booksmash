#!/usr/bin/env python
#
# Copyright (C) 2013 Federico Ceratto and others, see AUTHORS file.
# Released under GPLv3+ license, see LICENSE.txt
#
# Cork example web application
#
# The following users are already available:
#  admin/admin, demo/demo

import bottle
from beaker.middleware import SessionMiddleware
from cork import Cork
import logging
import os
import twitter
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
import getData
import requests
import Book

stemmer = PorterStemmer()

def tokenize(statuses):
  tokens = []
  for status in statuses:
    tokstatus = word_tokenize(status)
    for token in tokstatus:
      tokens.append(token)
  return tokens

def stemList(tokens):
  stems = []
  for token in tokens:
    stem = stemmer.stem(token.lower())
    stems.append(stem)
  return stems

logging.basicConfig(format='localhost - - [%(asctime)s] %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)
bottle.debug(True)

# Use users.json and roles.json in the local example_conf directory
aaa = Cork('example_conf')

app = bottle.app()
session_opts = {
    'session.cookie_expires': True,
    'session.encrypt_key': 'please use a random key and keep it secret!',
    'session.httponly': True,
    'session.timeout': 3600 * 24,  # 1 day
    'session.type': 'cookie',
    'session.validate_key': True,
}
app = SessionMiddleware(app, session_opts)


# #  Bottle methods  # #

def postd():
    return bottle.request.forms


def post_get(name, default=''):
    return bottle.request.POST.get(name, default).strip()

@bottle.post('/search')
def displayResults():
  api = twitter.Api(consumer_key='tGj4FIQtq1OcuE4HkFDag',
                  consumer_secret='Ii37iuXec8C7va4iUYWjGS9oD1natpZlAHKA2RVYNs',
                  access_token_key='240792557-Dw0Jsyo4BI8wy15GslZZdQqVrjzb30DHYSPacUoA',
                  access_token_secret='e2bVx7dfpVLMJYzUYfd46cpFIFSIqcrjYFR6SUTAE')
  username = bottle.request.forms.query
  if len(username.split(" ")) == 1:
    if not username[0] == "@":
      username = "@" + username
    try:
      statuses = api.GetUserTimeline(screen_name=username)
      statuses =  [s.text for s in statuses]
    except:
      statuses = []
  else:
    statuses = [username]
  tokens = tokenize(statuses)
  stems = stemList(tokens)
  
  books = getData.getSimilarity(stems, 'LSI')

  t = bottle.template('templates/results.tpl',q=username,r=statuses,b=books)
  return t

@bottle.route('/book/<isbn>')
def displayBook(isbn):
  aaa.require(fail_redirect='/login')
  uri = "http://api.harpercollins.com/api/v3/hcapim?apiname=ProductInfo&format=XML&isbn="+ str(isbn) + "&apikey=6wbqgghpzmxhmtf5dmykv2bj"
  r = requests.get(uri)
  b = Book.Book(r.text)
  t = bottle.template('templates/book.tpl',book=b)
  return t

@bottle.post('/login')
def login():
    """Authenticate users"""
    username = post_get('username')
    if len(username) == 0:
      username = "fail"
    password = post_get('password')
    aaa.login(username, password, success_redirect='/', fail_redirect='/login')

@bottle.route('/user_is_anonymous')
def user_is_anonymous():
    if aaa.user_is_anonymous:
        return 'True'

    return 'False'

@bottle.route('/logout')
def logout():
    aaa.logout(success_redirect='/login')

@bottle.route('/')
def index():
    """Only authenticated users can see this"""
    aaa.require(fail_redirect='/login')
    return bottle.template('templates/index.tpl')

    #return 'Welcome! <a href="/admin">Admin page</a> <a href="/logout">Logout</a>'

"""
@bottle.route('/restricted_download')
def restricted_download():
    aaa.require(fail_redirect='/login')
    return bottle.static_file('static_file', root='.')


@bottle.route('/my_role')
def show_current_user_role():
    session = bottle.request.environ.get('beaker.session')
    print "Session from simple_webapp", repr(session)
    aaa.require(fail_redirect='/login')
    return aaa.current_user.role

# Admin-only pages

@bottle.route('/admin')
@bottle.view('admin_page')
def admin():
    aaa.require(role='admin', fail_redirect='/sorry_page')
    return dict(
        current_user=aaa.current_user,
        users=aaa.list_users(),
        roles=aaa.list_roles()
    )
"""
# Static pages

@bottle.route('/login')
def login_form():
    """Serve login form"""
    return bottle.template('templates/login_form_booksmash')


@bottle.route('/sorry_page')
def sorry_page():
    """Serve sorry page"""
    return '<p>Sorry, you are not authorized to perform this action</p>'


@bottle.route('/static/:path#.+#', name='static')
def static(path):
    return bottle.static_file(path, root='static')

# #  Web application main  # #

def main():

    # Start the Bottle webapp
    bottle.debug(True)
    bottle.run(app=app, quiet=False, reloader=True, host="0.0.0.0", port=os.environ.get('PORT',5000))

if __name__ == "__main__":
    main()