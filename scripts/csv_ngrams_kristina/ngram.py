#ce programme crée un vocabulaire de 2 grams à partir d'un ensemble de documents
#le résultat est sauvegardé dans un fichier csv (two-grams.csv)
import re
import csv
from glob import glob
import spacy
from spacy import displacy
from nltk import ngrams
nlp = spacy.load("en_core_web_sm")

class Voc(object):
    def __init__(self, corpus):
        self.corpus = corpus
        self.voc = []
    def build_voc(self):
        for fic in self.corpus.lire():
            #print(fic)
            ficstring = self.clean(self.corpus.string(fic).replace('\n',' '))
            text = nlp(ficstring)
            n=2
            twograms=ngrams(text, n)
            for grams in twograms:
                    if(grams not in self.voc):
                            self.voc.append(grams)
            with open("two-grams.csv", "w") as f:
                        writer = csv.writer(f, delimiter="\n")
                        writer.writerow(self.voc)
        return "two-grams.csv"


     
    def clean(self, ficstring):
        ficstring = ficstring.replace('(', '')
        ficstring = ficstring.replace(')', '')
        ficstring = ficstring.replace('<','')
        ficstring = ficstring.replace('>','')
        ficstring = ficstring.replace('/','')
        ficstring = ficstring.replace(':','')
        ficstring = ficstring.replace('"','')
        ficstring = ficstring.replace('!','')
        ficstring = ficstring.replace('?','')
        ficstring = ficstring.replace('.','')
        ficstring = ficstring.replace('--','')
        ficstring = ficstring.replace(';','')
        ficstring = ficstring.replace('/br','')
        ficstring = ficstring.replace('br','')
        ficstring = ficstring.replace('.br','')
        return ficstring
    def ecrire_voc(self, out):
        out.write('\n'.join([elem for elem in self.voc]))
    def load_voc(self, vocfile):
        self.voc = Voc.string(vocfile)

class Corpus(object):
    def __init__(self, path, voc = ""):
        self.corpus = path
        if voc:
            self.voc = Voc.load_voc(voc)
        else:
            voc = Voc(self)
            voc.build_voc()
            self.voc = voc.voc
        self.bow = []
    def lire(self):
        return glob(self.corpus+"/*")
    def string(self, fic):
        return open(fic).read()

if __name__ == "__main__":
    c = Corpus('./cor/*')
    Voc(c) 
    
