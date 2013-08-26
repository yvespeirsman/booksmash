import os
from gensim import corpora, models, similarities

def readIDMap(f):
    idMap = {}
    i = open(f,'r')
    for line in i:
        line = line.strip().split("\t")
        id = int(line[0])
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

def readTopics(f):
    topics = {}
    i = open(f)
    for line in i:
        line = line.strip().split(',')
        topic = int(line[0])
        topicName = line[1]
        if len(topicName) > 1:
            topics[topic] = str(topic) + " - " + topicName
    i.close()
    return topics

def rescale(scores):
    newScores = []
    for (score, topic) in scores:
        score *= 200
        if score > 100:
            score = 100
        newScores.append((score, topic))
    return newScores
    

class Model():

    def __init__(self,modelName):

        self.dictionary = corpora.Dictionary.load(modelName + '.dict')
        if os.path.exists(modelName + '.lsi'):
            self.ids = readIDMap(modelName + '.ids')
            self.lsimodel = models.LsiModel.load(modelName + '.lsi')
            self.lsiindex = similarities.MatrixSimilarity.load(modelName+'LSIIndex.index')
        if os.path.exists(modelName + '.lda') and os.path.exists(modelName + '.topics'):
            self.ldamodel = models.LsiModel.load(modelName + '.lda')
            self.ldaindex = similarities.MatrixSimilarity.load(modelName+'LDAIndex.index')
            self.topics = readTopics(modelName + '.topics')

    def findSimilarDocuments(self, query, num):
        query_bow = self.dictionary.doc2bow(query)
        query_vec = self.lsimodel[query_bow]
        
        sims = self.lsiindex[query_vec]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        
        results = []
        for (book, sim) in sims:
            title = self.ids[book]["title"]
            author = self.ids[book]["author"]
            cover = self.ids[book]["cover"]
            isbn = self.ids[book]["isbn"]
            if len(title) > 2:
                results.append({"title":title, "author":author, "cover":cover,"isbn":isbn})
      
        return results[:num]

    def getTopics(self, query, num):
        query_bow = self.dictionary.doc2bow(query)
        query_vec = self.ldamodel[query_bow]
        
        topicScores = []
        for (topic, score) in query_vec:
            if self.topics.has_key(topic):
                topicScores.append((score, self.topics[topic]))
        topicScores.sort()
        topicScores.reverse()
        return rescale(topicScores[:3])