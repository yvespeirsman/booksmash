#!/usr/bin/python

from bottle import run, route, template, request, post, static_file, debug
import os
import twitter
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()

def tokenize(statuses):
  tokens = []
  for status in statuses:
    tokstatus = word_tokenize(status.text)
    for token in tokstatus:
      tokens.append(token)
  return tokens

def stemList(tokens):
  stems = []
  for token in tokens:
    stem = stemmer.stem(token.lower())
    stems.append(stem)
  return stems

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
  tokens = tokenize(statuses)
  stems = stemList(tokens)
  print statuses[0].text
  print stems
  t = template('templates/results.tpl',q=username,r=statuses)
  return t

@route('/')
def show():
  t = template('templates/index.tpl')
  return t

debug(True)
run(host="0.0.0.0", port = os.environ.get('PORT',5000))

