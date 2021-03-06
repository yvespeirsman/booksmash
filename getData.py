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
import Text

nltk.data.path.append('./nltk_data/') 
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

def getContentFromImprintsWithStemming():
    files = glob.glob("data/imprints/*.xml")
    documents = {}
    titlesDone = {}
    t = 0 
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
                        text = re.sub('<.*?>','',summaryText)
                        text = parser.unescape(text)
                  
                        sentences = sent_tokenize(text)
                        for sent in sentences:
                            tokens = word_tokenize(sent)
                            for token in tokens:
                                if not stoplist.has_key(token.lower()) and len(token.lower()) > 2:
                                    stem = stemmer.stem(token.lower())                                
                                    summaryTokens.append(stem)
                        t = t+1
                        print t
                        documents[t] = {}
                        documents[t]["title"] = title
                        documents[t]["isbn"] = isbn
                        documents[t]["author"] = author
                        documents[t]["fulltext"] = summaryTokens
                        documents[t]["cover"] = cover
    print "NUM:", len(documents.keys())

    return documents

def getContentFromImprints():
    files = glob.glob("data/imprints/*.xml")
    documents = {}
    titlesDone = {}
    t = 0
    #s = open('summariesAll.txt','w')
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
                                #if not stoplist.has_key(token.lower()) and len(token.lower()) > 2:
                                    if tag[0] == 'J':
                                        lemma = lemmatizer.lemmatize(token,wordnet.ADJ)
                                    elif tag[0] == 'N':
                                        lemma = lemmatizer.lemmatize(token,wordnet.NOUN)
                                    elif tag[0] == 'V':
                                        lemma = lemmatizer.lemmatize(token,wordnet.VERB)
                                        #stem = stemmer.stem(token.lower())                                
                                    else:
                                        lemma = lemmatizer.lemmatize(token)
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
                        #s.write(documents[t]["isbn"] + "\t" + " ".join(documents[t]["fulltext"]).encode('utf-8') + "\n")
    print "NUM:", len(documents.keys())

    #s.close()
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
            locale = root.find("Product_Detail").find('Locale_Desc')
            if locale is not None:
                localeText = locale.text
                if localeText == "US Trade" and not titlesDone.has_key(title):
                    titlesDone[title] = 1
                    seo = root.find("Product_Detail").find('Product_Group_SEO_Copy')
                    if seo is not None:
                        text = seo.text 
                        if text:
                            text = re.sub('<.*?>','',text)
                            text = parser.unescape(text)
                            sentences = sent_tokenize(text)
                            for sent in sentences:
                                tokens = word_tokenize(sent)
                                
                                for token in tokens:
                                    if not stoplist.has_key(token.lower()) and len(token.lower()) > 2:
                                        stem = stemmer.stem(token.lower())
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

def readBrown():
    print "reading corpus"
    files = glob.glob('/home/yves/Downloads/brown/c*')
    texts = []
    for f in files:
        text = []
        i = open(f)
        for line in i:
            line = line.strip().split()
            if len(line) > 0:
                for word in line:
                    word = word.split('/')
                    token = word[0].lower()
                    tag = word[-1]
                    if tag[0] in ['n','v','j'] and not tag[:2] == 'np':
                        if not token in stoplist and len(token) > 3:
                            stem = stemmer.stem(token)
                            text.append(stem)
        i.close()
        texts.append(text)
    print len(texts)
    return texts

def readBookContent():
    files = glob.glob('data/content/*.xml')
    texts = []
    for f in files:
        print f
        i = open(f)
        text = ""
        for line in i:
            line = line.strip()                         
            line = re.sub('<.*?>','',line)
            line = parser.unescape(line)
            try:
                text = text + " " + line.decode('utf-8')
            except:
                continue
        i.close()
    
        summaryTokens = []
        sentences = sent_tokenize(text)
        for sent in sentences:
            tokens = word_tokenize(sent)
            for token in tokens:
                if not stoplist.has_key(token.lower()) and len(token.lower()) > 3:
                    stem = stemmer.stem(token.lower())                                
                    summaryTokens.append(stem)
        if len(summaryTokens) > 20:
            texts.append(summaryTokens)
    i.close()
    return texts

def readWiki():
    texts = []
    i = open("/home/yves/Downloads/wiki.xml")
    summaryTokens = []
    t = 0
    for line in i:
        if line[:4] == '<doc':
            t = t+1
            print t, line
            if len(summaryTokens) > 1:
                texts.append(summaryTokens)
            summaryTokens = []
        else:
            line = line.strip()                         
            sentences = sent_tokenize(line)

            for sent in sentences:
                tokens = word_tokenize(sent)
                for token in tokens:
                    if not stoplist.has_key(token.lower()) and len(token.lower()) > 3:
                        stem = stemmer.stem(token.lower())                                
                        summaryTokens.append(stem)
    i.close()
    return texts

def removeLowFreq(texts):
    print "removing low frequencies"
    freqs = {}
    for text in texts:
        for word in text:
            if freqs.has_key(word):
                freqs[word] = freqs[word] + 1
            else:
                freqs[word] = 1

    newTexts = []
    for text in texts:
        newText = []
        for word in text:
            if freqs.has_key(word) and freqs[word] > 2:
                newText.append(word)
        newTexts.append(newText)
    return newTexts


def modelWiki():
    texts = readWiki()
    texts = removeLowFreq(texts)
    print "making dictionary"

    dictionary = corpora.Dictionary(texts)
    dictionary.save('wiki.dict')

    print "making corpus"
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize('wiki.mm', corpus) 
    
    """
    dictionary = corpora.Dictionary.load('wiki.dict')
    corpus = corpora.MmCorpus('wiki.mm')
    """

    print "modelling corpus"
    lda = models.ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=100, passes=3)
    corpus_lda = lda[corpus]
    lda.print_topics(100, topn=50)
    lda.save('wiki.lda')

    print "computing similarities"
    indexLDA = similarities.MatrixSimilarity(lda[corpus])
    indexLDA.save('wiki.index')

def modelBrown():
    texts1 = readBrown()
    texts2 = readBookContent()
    print len(texts1)
    print len(texts2)

    texts = texts1 + texts2
    print len(texts)
    
    print "making dictionary"
    dictionary = corpora.Dictionary(texts)
    dictionary.save('brown.dict')

    print "making corpus"
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize('brown.mm', corpus) 

    print "modelling corpus"
    lda = models.ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=100, passes=50)
    corpus_lda = lda[corpus]
    lda.print_topics(100, topn=50)
    lda.save('brown.lda')

    print "computing similarities"
    indexLDA = similarities.MatrixSimilarity(lda[corpus])
    indexLDA.save('brown.index')


def model(documents):

    #documents = filter(documents)
    texts = []
    idMap = {}
    """
    sums = {}
    i = open('summariesAll.txt')
    for line in i:
        line = line.strip().split('\t')
        isbn = line[0]
        s = line[1].split()
        st = []
        for token in s:
            word = token.split("/")[0]
            tag = token.split("/")[-1]
            if not word in stoplist and len(word) > 3: 
                if tag[0] in ['J','N','V']:
                    st.append(word + '/' + tag[0])
        sums[isbn] = st
    i.close()
    """

    o = open('idMap.txt','w')
    t = 0
    for f in documents:
        idMap[t] = f
        title = documents[f]["title"]
        isbn = documents[f]["isbn"]

        #texts.append(sums[isbn])
        texts.append(documents[f]["fulltext"])

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

    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    

    print "----------------------------"
    print "LSA"
    print "----------------------------"

    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary,num_topics=100)
    corpus_lsi = lsi[corpus_tfidf]
    lsi.save('books.lsi')
    lsi.print_topics(100)
    indexLSI = similarities.MatrixSimilarity(lsi[corpus])
    indexLSI.save('booksLSIIndex.index')

    """
    print "----------------------------"
    print "LDA"
    print "----------------------------"

    lda = models.ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=100, passes=50)
    corpus_lda = lda[corpus]
    lda.print_topics(100)
    lda.save('books.lda')


    indexLDA = similarities.MatrixSimilarity(lda[corpus])
    indexLDA.save('booksLDAIndex.index')

    #index = similarities.MatrixSimilarity.load('test.index')

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

def findBestTopics(vec):
    topicScores = []
    for (topic, score) in vec:
        topicScores.append((score, topic))
    topicScores.sort()
    topicScores.reverse()
    return topicScores

topicNames = {}
i = open('topics.csv')
for line in i:
    line = line.strip().split('\t')
    t = line[0]
    name = line[1]
    topicNames[int(t)] = name
i.close()            

def resize(topics, num):
    resizedTopics = []
    for (val, topic) in topics[:num]:
        val = val*100
        val = val*2
        if val > 100:
            val = 100
        if topicNames.has_key(topic):
            resizedTopics.append((val, topicNames[topic]))
        else:
            resizedTopics.append((val, topic))
    print resizedTopics
    return resizedTopics

def readIDMap():
    idMap = {}
    i = open('model/idMap.txt','r')
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
    return idMap


def getSimilarityForTopic(topic):
    idMap = readIDMap()
    dictionary = corpora.Dictionary.load('model/books.dict')
    model = models.LdaModel.load('model/books.lda')
    index = similarities.MatrixSimilarity.load('model/booksLDAIndex.index')

    query_vec = []
    for x in range(0,100):
        if x == topic:
            query_vec.append((x,1))
  
    sims = index[query_vec]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
  
    results = []
    print sims[:5]
    for (book, sim) in sims[:5]:
        title = idMap[book]["title"]
        author = idMap[book]["author"]
        cover = idMap[book]["cover"]
        isbn = idMap[book]["isbn"]
        #print sim, title, author
        if len(title) > 2:
            results.append({"title":title, "author":author, "cover":cover,"isbn":isbn})
    print results

def getSimilarity(query_stems, method):

    idMap = readIDMap()

    dictionary = corpora.Dictionary.load('model/books.dict')
    #corpus = corpora.MmCorpus('model/bookcorpus.mm')
    if method == "LSI":
        model = models.LsiModel.load('model/books.' + str(method).lower())
        #model.print_topics(100,num_words=100)
    elif method == "LDA":
        model = models.LdaModel.load('model/books.' + str(method).lower())
        #model.print_topics(200,topn=100)
    index = similarities.MatrixSimilarity.load('model/books'+str(method)+'Index.index')

    query_bow = dictionary.doc2bow(query_stems)
    query_vec = model[query_bow]
    bestTopics = findBestTopics(query_vec)
    print bestTopics

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

    bestTopicsResized = resize(bestTopics,3)
    return (bestTopicsResized,results[:12])

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
    model = models.LsiModel.load('brown.lda')
    model.print_topics(100,topn=50) #num_words

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

def getBookContent():

    done = {}
    fs = glob.glob('data/books/*')
    for f in fs:
        isbn = f.split('-')[1]
        isbn = isbn.split('.')[0]
        done[isbn] = 1 

    isbns = []
    i = open('model/books.ids')
    for line in i:
        line = line.strip().split('\t')
        isbn = line[3]
        if not isbn in done:
            isbns.append(isbn)
        else:
            print "isbn", isbn, "done"
    i.close()

    random.shuffle(isbns)
    for isbn in isbns[:4000]:

        uri = "http://api.harpercollins.com/api/v3/hcapim?apiname=HC_Text&format=XML&isbn="+isbn+"&apikey=6wbqgghpzmxhmtf5dmykv2bj"
        oFile = "data/content/" + isbn + ".xml"
        if not os.path.exists(oFile):
            print isbn
            os.system('curl "' + uri + '" > ' + oFile)


#readTopics()

#getLocales()
#getImprints()
#getAuthors()
#getBooks()
"""
b = getContent()
a = getContentFromImprintsWithStemming()

ab = {}
t = 0
isbns = {}
for key in a:
    ab[t] = a[key]
    t = t+1

for key in b:
    isbn = b[key]["isbn"]
    if not isbn in isbns:
        isbns[isbn] = 1
        t = t+1
        ab[t] = b[key]

print len(ab.keys()), "documents"
model(ab)
"""
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

#readBookContent()
modelWiki()
#writeTopics()
#getBookContent()

