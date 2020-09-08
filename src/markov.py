import random
import _pickle as cPickle

class MarkovBot:
    MAXGEN = 1000
    NONWORD = '\n'

    def __init__(self, location):
        dataFile = open(location, 'rb')
        self.dict = cPickle.load(dataFile, encoding='latin1')
        return

    def generate(self):
        word1 = self.NONWORD
        word2 = self.NONWORD
        text = ""

        for i in range(self.MAXGEN):
            if (word1,word2) not in self.dict:
                successorList = random.choice(self.dict.keys())
            else:
                successorList = self.dict[(word1,word2)]

            word3 = random.choice(successorList)

            if word3 == self.NONWORD:
                break

            text = text + " " + word3
            word1, word2 = word2, word3

        return text