#!/usr/bin/python

from bottle import run, route, template, request, post, static_file, debug
import os
import twitter

@post('/search')
def displayResults():
  api = twitter.Api(consumer_key='tGj4FIQtq1OcuE4HkFDag',
                  consumer_secret='Ii37iuXec8C7va4iUYWjGS9oD1natpZlAHKA2RVYNs',
                  access_token_key='240792557-Dw0Jsyo4BI8wy15GslZZdQqVrjzb30DHYSPacUoA',
                  access_token_secret='e2bVx7dfpVLMJYzUYfd46cpFIFSIqcrjYFR6SUTAE')
  username = request.forms.query
  print username
  statuses = api.GetUserTimeline(screen_name=username)
  print [s.text for s in statuses]
  print statuses[0].text
  t = template('templates/results.tpl',q=username,r=statuses)
  return t

@route('/')
def show():
  t = template('templates/index.tpl')
  return t

debug(True)
run(host="0.0.0.0", port = os.environ.get('PORT',5000))

