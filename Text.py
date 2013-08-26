import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer

nltk.data.path.append('./nltk_data/')
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

class Text():
    
    def __init__(self,string):
        self.string = string

    def tokenize(self):
        self.tokens = []
        sentences = sent_tokenize(self.string)
        for sent in sentences:
            toks = word_tokenize(sent)
            for token in toks:
                self.tokens.append(token)


    def stem(self):
        if self.tokens:
            self.stems = []
            stems = []
            for token in self.tokens:
                stem = stemmer.stem(token.lower())
                self.stems.append(stem)
           

    def lemmatize(self):
        if self.tokens:
            self.lemmas = []
        
            tags = nltk.pos_tag(self.tokens)
            for (token, tag) in tags:
                if tag[0] == 'A':
                    lemma = lemmatizer.lemmatize(token,wordnet.ADJ)
                elif tag[0] == 'N':
                    lemma = lemmatizer.lemmatize(token,wordnet.NOUN)
                elif tag[0] == 'V':
                    lemma = lemmatizer.lemmatize(token,wordnet.VERB)
                else:
                    lemma = lemmas.lemmatize(token)
                self.lemmas.append(lemma.lower() + "/" + tag)
