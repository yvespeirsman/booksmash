import xml.etree.ElementTree as ET
import os
import time
import glob
import re
import HTMLParser
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
from gensim import corpora, models, similarities
import logging
import random

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', filename="log.txt", level=logging.INFO)
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

def getAuthors():
    tree = ET.parse('data/perennial_ustrade_authors.xml')
    root = tree.getroot()

    authors = {}

    for el in root.iter('Contributor_List'):
        author = el.find('Contributor_Persona_ID').text
        info = el.find('Contributor_Detail_URI').text
        print author, info
        """
        for author in el.iter('Contributor_Persona_ID'):
            print author.text
            authors[author.text] = 1
        """
    authorList = authors.keys()
    authorList.sort()

    """
    for author in authorList[3229:5000]:
        print '--', author
        uri = "http://api.harpercollins.com/api/v3/hcapim?apiname=catalog&format=XML&authorglobalid="+str(author)+"&apikey=6wbqgghpzmxhmtf5dmykv2bj" 
   
        os.system('curl "' + uri + '" > data/authors/' + str(author) + '.xml')
    """
    
      
def stemList(tokens):
    stems = []
    for token in tokens:
        stem = stemmer.stem(token.lower())
        stems.append(stem)
    return stems


def getBooks():
    files = glob.glob("data/perennial*.xml")
    t = 0
    random.shuffle(files)
    stop = 0
    for f in files:
      if stop == 0:
        books = []
        author = f[13:-4]
        try:
            tree = ET.parse(f)
            root = tree.getroot()
        except:
            continue
        for el in root.iter('Products'):
            isbn = el.find('ISBN').text
            date = el.find('On_Sale_Date').text
            imprint = el.find('Imprint').text
            form = el.find('Format').text
            print isbn, imprint, form
            if re.search('back', form):
                if date:
                    year = int(date.split(' ')[0].split('/')[2])
                    if year > 9 and year < 14:
                        books.append(isbn)
        books = list(set(books))
        print "found", len(books), "books"

        for isbn in books:
            oFile = "data/books/" + str(author) +"-"+ str(isbn) + ".xml"
            print isbn, oFile
            if not os.path.isfile(oFile):
                uri = "http://api.harpercollins.com/api/v3/hcapim?apiname=ProductInfo&format=XML&isbn="+ str(isbn) + "&apikey=6wbqgghpzmxhmtf5dmykv2bj"

                os.system('curl "' + uri + '" > ' + oFile)
                t = t+1
            else:
                print "already exists"
            print t
        if t >= 48000:
            stop = 1
            break

parser = HTMLParser.HTMLParser()
stemmer = PorterStemmer()

def getContentFromImprints():
    files = glob.glob("data/imprints/*.xml")
    documents = {}
    titlesDone = {}
    t = 0
    s = open('summaries.txt','w')
    done = 0
    for f in files:
        print f, t
        try:
            tree = ET.parse(f)
        except:
            continue
        root = tree.getroot()

        for product in root.iter('Product_Group'):
            title = product.find('Products').find('Title').text
            titleS = re.sub("\s[A-Z]+\s?$","",title)
            titleS = re.sub("[Tt]he","",titleS)
            titleS = re.sub(",","",titleS)
            titleS = re.sub(" ", "", titleS)
            titleS = titleS.strip().lower()
            if titleS in titlesDone:
                done = done+1
                print titleS, "DONE", done
            else:

                titlesDone[titleS] = 1

                isbn = product.find('Products').find('ISBN').text
                author = product.find('Products').find('Author1').text
                summary = product.find('Product_Group_SEO_Copy')
                cover = product.find('Products').find("CoverImageURL_Medium").text
                if summary is not None:
                    summaryText = summary.text 
                    if summaryText is not None and len(summaryText.split()) > 20:

                        summaryTokens = []
                        """
                        text = re.sub('<.*?>','',summaryText)
                        text = parser.unescape(text)
                        sentences = sent_tokenize(text)
                        for sent in sentences:
                            tokens = word_tokenize(sent)
                            tags = nltk.pos_tag(tokens)
                            for (token,tag) in tags:
                                if not stoplist.has_key(token.lower()) and len(token.lower()) > 2:
                                    if tag[0] == 'A':
                                        lemma = lemmatizer.lemmatize(token,wordnet.ADJ)
                                        summaryTokens.append(lemma.lower() + '/' + tag)
                                    elif tag[0] == 'N':
                                        lemma = lemmatizer.lemmatize(token,wordnet.NOUN)
                                        summaryTokens.append(lemma.lower() + '/' + tag)
                                    elif tag[0] == 'V':
                                        lemma = lemmatizer.lemmatize(token,wordnet.VERB)
                                        #stem = stemmer.stem(token.lower())                                
                                        summaryTokens.append(lemma.lower() + '/' + tag)
                        """
                        t = t+1
                        print t
                        documents[t] = {}
                        documents[t]["title"] = title
                        documents[t]["isbn"] = isbn
                        documents[t]["author"] = author
                        documents[t]["fulltext"] = summaryTokens
                        documents[t]["cover"] = cover
                        s.write(documents[t]["isbn"] + "\t" + " ".join(documents[t]["fulltext"]).encode('utf-8') + "\n")
    print "NUM:", len(documents.keys())

    s.close()
    return documents

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
                            #print title, "==", text
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
            if len(document) > 20:
                documents[f] = {}
                documents[f]["title"] = title
                documents[f]["isbn"] = isbn
                documents[f]["author"] = author
                documents[f]["fulltext"] = document
                documents[f]["cover"] = cover
    print "NUM:", len(documents.keys())
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

    sums = {}
    i = open('summaries1.txt')
    for line in i:
        line = line.strip().split('\t')
        isbn = line[0]
        s = line[1].split()
        st = []
        for token in s:
            word = token.split("/")[0]
            tag = token.split("/")[-1]
            st.append(word + '/' + tag[0])
        sums[isbn] = st
    i.close()
    
    o = open('idMap.txt','w')
    t = 0
    for f in documents:
        idMap[t] = f
        title = documents[f]["title"]
        isbn = documents[f]["isbn"]

        texts.append(sums[isbn])
        
        author = documents[f]["author"]
        cover = documents[f]["cover"]
        if cover is None:
            cover = "NOCOVER"
        #print title, isbn

        try:
            o.write(str(t) + "\t" + str(f) + "\t" + title.encode('ascii','xmlcharrefreplace') + "\t" + isbn + "\t" + author + "\t" + cover + "\n")
        except:
            o.write(str(t) + "\t" + str(f) + "\tX\tY\tZ\tQ\n")
        t += 1
    o.close()

    dictionary = corpora.Dictionary(texts)
    dictionary.save('books.dict')

    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize('bookcorpus.mm', corpus) 

    #tfidf = models.TfidfModel(corpus)
    #corpus_tfidf = tfidf[corpus]
    

    print "----------------------------"
    print "LSA"
    print "----------------------------"

    #lsi = models.LsiModel(corpus_tfidf, id2word=dictionary,num_topics=100)
    #corpus_lsi = lsi[corpus_tfidf]
    #lsi.save('books.lsi')
    #lsi.print_topics(100)

    print "----------------------------"
    print "LDA"
    print "----------------------------"

    lda = models.ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=100, passes=50)
    corpus_lda = lda[corpus]
    lda.print_topics(100)
    lda.save('books.lda')


    #indexLSI = similarities.MatrixSimilarity(lsi[corpus])
    #indexLSI.save('booksLSIIndex.index')
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
        model.print_topics(100,num_words=100)
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
    for (book, sim) in sims:
        title = idMap[book]["title"]
        author = idMap[book]["author"]
        cover = idMap[book]["cover"]
        isbn = idMap[book]["isbn"]
        #print sim, title, author
        if len(title) > 2:
            results.append({"title":title, "author":author, "cover":cover,"isbn":isbn})
    return results[:12]

def getImprints():
    d = {}
    files = glob.glob('data/authors/*.xml')
    for f in files:
        try:
            tree = ET.parse(f)
        except:
            continue   
        root = tree.getroot()
        for imprint in root.iter('Imprint'):
            d[imprint.text] = 1
    print d.keys()

    for imprint in d.keys():
        imp1 = re.sub(' ', '%20', imprint)
        uri = "http://api.harpercollins.com/api/v3/hcapim?apiname=catalog&format=XML&imprint="+ imp1 +"&locale=US+Trade&apikey=6wbqgghpzmxhmtf5dmykv2bj"
        print imprint, imp1, uri
        imp = re.sub(' ', '_', imprint)
        fOut = imp + '_USTrade.xml'
        os.system('curl "' + uri + '" > data/imprints/' + fOut)

def getLocales():
    d = {}
    files = glob.glob('data/authors/*.xml')
    for f in files:
        try:
            tree = ET.parse(f)
        except:
            continue   
        root = tree.getroot()
        for imprint in root.iter('Locale_Desc'):
            d[imprint.text] = 1
    print d.keys()

def writeTopics():
    model = models.LsiModel.load('books.lda')
    model.print_topics(100,topn=100) #num_words

def readTopics():
    i = open('log.txt')
    for line in i:
        line = line.strip().split()
        for t in line:
            if not t[0] == '-':
                if len(t.split('*')) > 1:
                    print t.split('*')[1],
                else:
                    print t,
        print "\n"
    i.close()

#readTopics()

#getLocales()
#getImprints()
#getAuthors()
#getBooks()
#getContentFromImprints()

#query = "trade economy finance currency money international market".split()
#query = "cancer illness hospital ill critical drugs medecine".split()
#query = "dark middle ages castle king queen dragon knight".split()
#query_stems = stemList(query)
#print query_stems
#documents = getContentFromImprints()
#model(documents)
#writeTopics()


#getSimilarity(query_stems)
# todo: remove stopwords
# todo: more authors
