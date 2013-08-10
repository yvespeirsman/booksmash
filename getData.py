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

    for author in authorList[1000:2000]:
        print '--', author
        uri = "http://api.harpercollins.com/api/v3/hcapim?apiname=catalog&format=XML&authorglobalid="+str(author)+"&apikey=6wbqgghpzmxhmtf5dmykv2bj" 
   
        os.system('curl "' + uri + '" > data/authors/' + str(author) + '.xml')

#getAuthors() 
      
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
    teller = 0
    titlesDone = {}
    for f in files:
        teller = teller + 1
        print f,teller
        
        document = []
        try:
            tree = ET.parse(f)
        except:
            continue
        root = tree.getroot()
        if root.find("Product_Detail") is not None:

            title = root.find("Product_Detail").find("Title").text
            title = re.sub("\s[A-Z]+\s?$","",title)
            title = title.strip()
            author = root.find("Product_Detail").find("Product_Contributors").find("Product_Contributor").find("Display_Name").text
            isbn = root.find("Product_Detail").find("ISBN").text
            cover = root.find("Product_Detail").find("CoverImageURL_Medium").text
            if root.find('Imprint') != "Rayo" and not titlesDone.has_key(title):
                titlesDone[title] = 1
                for el in root.iter("Product_Content"):
                    t = el.find('Content_Type_ID').text
                    if t == "605": # 605 is summary
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
                                    if not stoplist.has_key(token.lower()) and len(token.lower()) > 2:
                                        stem = stemmer.stem(token.lower())
                                        #print token, "-->", stem
                                        document.append(stem)
            documents[f] = {}
            documents[f]["title"] = title
            documents[f]["isbn"] = isbn
            documents[f]["author"] = author
            documents[f]["fulltext"] = document
            documents[f]["cover"] = cover
    return documents

i = open("english-stop-words-and-names.txt")
stoplist = {}
for line in i:
    stoplist[line.strip().lower()] = 1
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

    #documents = filter(documents)
    texts = []
    idMap = {}
    
    o = open('idMap.txt','w')
    t = 0
    for f in documents:
        texts.append(documents[f]["fulltext"])
        idMap[t] = f
        title = documents[f]["title"]
        isbn = documents[f]["isbn"]
        author = documents[f]["author"]
        cover = documents[f]["cover"]
        if cover is None:
            cover = "NOCOVER"
        print title, isbn
        o.write(str(t) + "\t" + f + "\t" + title.encode('ascii','xmlcharrefreplace') + "\t" + isbn + "\t" + author + "\t" + cover + "\n")
        t += 1
    o.close()

    dictionary = corpora.Dictionary(texts)
    dictionary.save('books.dict')

    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize('bookcorpus.mm', corpus) 

    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    

    print "----------------------------"
    print "LSA"
    print "----------------------------"

    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary,num_topics=200)
    corpus_lsi = lsi[corpus_tfidf]
    lsi.save('books.lsi')
    lsi.print_topics(200)

    print "----------------------------"
    print "LDA"
    print "----------------------------"

    lda = models.ldamodel.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=200)
    corpus_lda = lda[corpus_tfidf]
    lda.print_topics(200)
    lda.save('books.lda')


    indexLSI = similarities.MatrixSimilarity(lsi[corpus])
    indexLSI.save('booksLSIIndex.index')
    indexLDA = similarities.MatrixSimilarity(lda[corpus])
    indexLDA.save('booksLDAIndex.index')

    #index = similarities.MatrixSimilarity.load('test.index')
    """
    #print query_stems
    query_bow = dictionary.doc2bow(query_stems)
    print query_bow
    query_vec = lsi[query_bow]
    print query_vec
    sims = index[query_vec]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    for (book, sim) in sims[:10]:
        f = idMap[book]
        print sim, documents[f]["title"]
    """

def getSimilarity(query_stems, method):

    idMap = {}
    i = open('idMap.txt','r')
    for line in i:
        line = line.strip().split("\t")
        id = int(line[0])
        f = line[1]
        title = line[2]
        isbn = line[3]
        author = line[4]
        cover = line[5]
        idMap[id] = {}
        idMap[id]["title"] = title
        idMap[id]["author"] = author
        idMap[id]["cover"] = cover
        idMap[id]["isbn"] = isbn
    i.close()

    dictionary = corpora.Dictionary.load('model/books.dict')
    #corpus = corpora.MmCorpus('model/bookcorpus.mm')
    if method == "LSI":
        model = models.LsiModel.load('model/books.' + str(method).lower())
        #model.print_topics(200,num_words=100)
    elif method == "LDA":
        model = models.LdaModel.load('model/books.' + str(method).lower())
        #model.print_topics(200,topn=100)
    index = similarities.MatrixSimilarity.load('model/books'+str(method)+'Index.index')

    query_bow = dictionary.doc2bow(query_stems)
    #print query_bow
    query_vec = model[query_bow]
    #print query_vec
    sims = index[query_vec]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    #print "----------------"
    #print "similar docs"
    results = []
    for (book, sim) in sims[:10]:
        title = idMap[book]["title"]
        author = idMap[book]["author"]
        cover = idMap[book]["cover"]
        isbn = idMap[book]["isbn"]
        #print sim, title, author
        results.append({"title":title, "author":author, "cover":cover,"isbn":isbn})
    return results

#getAuthors()
#getBooks()

#query = "trade economy finance currency money international market".split()
#query = "cancer illness hospital ill critical drugs medecine".split()
#query = "dark middle ages castle king queen dragon knight".split()
#query_stems = stemList(query)
#print query_stems
#documents = getContent()
#model(documents)


#getSimilarity(query_stems)
# todo: remove stopwords
# todo: more authors
