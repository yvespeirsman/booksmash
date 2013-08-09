#!/usr/bin/python

from bottle import run, route, template, request, post, static_file, debug
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

@post('/search')
def displayResults():
  api = twitter.Api(consumer_key='tGj4FIQtq1OcuE4HkFDag',
                  consumer_secret='Ii37iuXec8C7va4iUYWjGS9oD1natpZlAHKA2RVYNs',
                  access_token_key='240792557-Dw0Jsyo4BI8wy15GslZZdQqVrjzb30DHYSPacUoA',
                  access_token_secret='e2bVx7dfpVLMJYzUYfd46cpFIFSIqcrjYFR6SUTAE')
  username = request.forms.query
  if not username[0] == "@":
    username = "@" + username
  print username
  statuses = api.GetUserTimeline(screen_name=username)
  statuses =  [s.text for s in statuses]
  tokens = tokenize(statuses)
  stems = stemList(tokens)
  print stems
  
  books = getData.getSimilarity(stems, 'LDA')
  print books

  t = template('templates/results.tpl',q=username,r=statuses,b=books)
  return t

@route('/book/<isbn>')
def displayBook(isbn):
  uri = "http://api.harpercollins.com/api/v3/hcapim?apiname=ProductInfo&format=XML&isbn="+ str(isbn) + "&apikey=6wbqgghpzmxhmtf5dmykv2bj"
  r = requests.get(uri)
  b = Book.Book(r.text)
  t = template('templates/book.tpl',book=b)
  return t
  

@route('/')
def show():
  t = template('templates/index.tpl')
  return t

debug(True)
run(host="0.0.0.0", port = os.environ.get('PORT',5000))

