import xml.etree.ElementTree as ET
import os
import time
import glob
import re
import HTMLParser
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models, similarities
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
stemmer = PorterStemmer()

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
       
def stemList(tokens):
    stems = []
    for token in tokens:
        stem = stemmer.stem(token.lower())
        stems.append(stem)
    return stems


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
    documents = {}
    for f in files:
        print f
        document = []
        try:
            tree = ET.parse(f)
        except:
            break
        root = tree.getroot()

        title = root.find("Product_Detail").find("Title").text
        isbn = root.find("Product_Detail").find("ISBN").text
        if root.find('Imprint') != "Rayo":

            for el in root.iter("Product_Content"):
                t = el.find('Content_Type_ID').text
                #if t == "609": # 605 is summary
                text = el.find('Content_Area1').text
                if text:
                    text = re.sub('<.*?>','',text)
                    text = parser.unescape(text)
                    #print text
                    sentences = sent_tokenize(text)
                    for sent in sentences:
                        tokens = word_tokenize(sent)
                        #print sent
                        #print tokens
                        for token in tokens:
                            stem = stemmer.stem(token.lower())
                            #print token, "-->", stem
                            document.append(stem)
        documents[f] = {}
        documents[f]["title"] = title
        documents[f]["isbn"] = isbn
        documents[f]["fulltext"] = document
    return documents

i = open("english-stop-words.txt")
stoplist = {}
for line in i:
    stoplist[line.strip()] = 1
i.close()

def filter(documents):
    for f in documents:
        textNoStop = []
        for word in documents[f]["fulltext"]:
            if not word in stoplist and len(word) > 2:
                textNoStop.append(word)
        documents[f]["fulltext-no-stop"] = textNoStop
    return documents

def model(documents):

    documents = filter(documents)
    texts = []
    idMap = {}
    
    t = 0
    for f in documents:
        texts.append(documents[f]["fulltext-no-stop"])
        idMap[t] = f
        t += 1

    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    print "----------------------------"
    print "LSA"
    print "----------------------------"

    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary,num_topics=100)
    corpus_lsi = lsi[corpus_tfidf]
    lsi.print_topics(100)

    print "----------------------------"
    print "LDA"
    print "----------------------------"

    lda = models.ldamodel.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=100)
    corpus_lda = lda[corpus_tfidf]
    lda.print_topics(100)

    index = similarities.MatrixSimilarity(lsi[corpus])
    #index.save('test.index')
    #index = similarities.MatrixSimilarity.load('test.index')

    #query = "trade economy finance currency money international market".split()
    #query = "cancer illness hospital ill critical drugs medecine".split()
    query = "police crime detective steal investigate criminal arrest judge".split()
    query_stems = stemList(query)
    print query_stems
    query_bow = dictionary.doc2bow(query_stems)
    print query_bow
    query_vec = lsi[query_bow]
    print query_vec
    sims = index[query_vec]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    for (book, sim) in sims:
        f = idMap[book]
        print sim, documents[f]["title"]

#getAuthors()
#getBooks()
documents = getContent()
model(documents)

# todo: remove stopwords

