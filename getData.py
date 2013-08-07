import xml.etree.ElementTree as ET
import os
import time
import glob
import re
import HTMLParser
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.porter import PorterStemmer

def getAuthors():
    tree = ET.parse('data/hc_authors.xml')
    root = tree.getroot()

    authors = {}

    for el in root.iter('Contributor_List'):
        for author in el.iter('Contributor_Persona_ID'):
            print author.text
            authors[author.text] = 1

    authorList = authors.keys()
    authorList.sort()

    for author in authorList[100:1000]:
        print '--', author
        uri = "http://api.harpercollins.com/api/v3/hcapim?apiname=catalog&format=XML&authorglobalid="+str(author)+"&apikey=6wbqgghpzmxhmtf5dmykv2bj" 
   
        os.system('curl "' + uri + '" > data/products/' + str(author) + '.xml')
       
def getBooks():
    files = glob.glob("data/authors/*.xml")
    for f in files:
        books = []
        author = f[13:-4]
        tree = ET.parse(f)
        root = tree.getroot()

        for el in root.iter('ISBN'):
            books.append(el.text)
        books = list(set(books))

        for isbn in books:
            oFile = "data/books/" + str(author) +"-"+ str(isbn) + ".xml"
            print isbn, oFile
            if not os.path.isfile(oFile):
                uri = "http://api.harpercollins.com/api/v3/hcapim?apiname=ProductInfo&format=XML&isbn="+ str(isbn) + "&apikey=6wbqgghpzmxhmtf5dmykv2bj"

                os.system('curl "' + uri + '" > ' + oFile)
            else:
                print "already exists"

parser = HTMLParser.HTMLParser()
stemmer = PorterStemmer()

def getContent():
    files = glob.glob("data/books/*.xml")
    for f in files:
        tree = ET.parse(f)
        root = tree.getroot()
        if root.find('Imprint') != "Rayo":

            for el in root.iter("Product_Content"):
                t = el.find('Content_Type_ID').text
                #if t == "609": # 605 is summary
                text = el.find('Content_Area1').text
                if text:
                    text = re.sub('<.*?>','',text)
                    text = parser.unescape(text)
                    print text
                    sentences = sent_tokenize(text)
                    for sent in sentences:
                        tokens = word_tokenize(sent)
                        print sent
                        print tokens
                        for token in tokens:
                            stem = stemmer.stem(token.lower())
                            print token, "-->", stem


#getAuthors()
#getBooks()
getContent()
