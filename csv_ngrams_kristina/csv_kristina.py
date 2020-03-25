#ce programme crée un vocabulaire à partir d'un ensemble de documents
#et sauvegarde les résultats dans un fichier csv (voc.csv)
#ensuite ce fichier sera utilisé dans la fonction getBOW() pour créer le sac de mots
import re
import csv
from glob import glob
import spacy
from spacy import displacy
nlp = spacy.load("en_core_web_sm")

class Voc(object):
    
    def __init__(self, corpus):
        self.corpus = corpus
        self.voc = []
        
    def build_voc(self):
        for fic in self.corpus.lire():
         
            ficstring = self.clean(self.corpus.string(fic).replace('\n',' '))
            text = nlp(ficstring)
       
            for token in text:
                if(token.text.lower() not in self.voc):
                    self.voc.append(token.text.lower())
        with open("voc.csv", "w") as f:
                writer = csv.writer(f,delimiter = "\n")
                writer.writerow(self.voc)
               
     
    def clean(self, ficstring):
      
        patt = re.compile('<[^>]+>')
        ficstring = ficstring.replace('(', '')
        ficstring = ficstring.replace(')', '')
        ficstring = re.sub(patt, ' ', ficstring)
        ficstring = re.sub('\.', r'. ', ficstring)
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
    
    def getBOW(self):
        x = 0
        with open("voc.csv", "r") as review:
            v=review.read()
            voc=v.split()
            
            for fic in self.lire():
                liste=[]
                for mot in fic:
                    if mot in voc:
                        liste.append("1")
                    else:
                        liste.append("0")
                self.bow.append(liste)
            with open("bow.csv", "w") as f:
                writer = csv.writer(f,delimiter = "\n")
                for mot in self.bow:
                    writer.writerow(mot)
            

if __name__ == "__main__":
    c = Corpus('./cor/*')
    b = c.getBOW()






        
