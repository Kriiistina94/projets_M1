from glob import glob

import re
import nltk
import math
from nltk.util import bigrams
from nltk.util import trigrams
import spacy
from spacy import displacy
nlp = spacy.load('en_core_web_sm')

class Voc(object) :

	def __init__(self, corpus) :

		self.corpus = corpus
		self.voc = []
		self.bigram=set()
		self.trigram=set()

	def build_voc(self) :
		for fic in self.corpus.lire() :
			ficstring = self.clean(self.corpus.string(fic).replace('\n',' '))
			string_nlp=nlp(ficstring)
			for item in string_nlp:
				if not item.is_space and not item.is_punct and str(item) not in self.voc:
					self.voc.append(str(item))

			self.bigram.update({' '.join((str(a), str(b))) for a, b in list(nltk.bigrams(string_nlp))})
			self.trigram.update({' '.join((str(a), str(b), str(c))) for a, b, c in list(nltk.trigrams(string_nlp))})

		self.bigram=list(self.bigram)
		self.trigram=list(self.trigram)




	def clean(self,ficstring) :
		ficstring = re.sub('(<[^>]*>)|\(|\)',' ',ficstring)
		ficstring = re.sub(' {2,}',' ',ficstring)
		return ficstring


	def ecrire_voc(self,out) :

		out.write('\n'.join([elem for elem in self.voc]))

	def load_voc(self, vocfile) :

		self.voc = vocfile

class VocCSV(Voc) :

	def __init__(self, corpus) :
		Voc.__init__(self, corpus)


class Corpus(object) :

	def __init__(self, path, voc = "") :

		self.corpus = path
		if voc :
			self.voc = voc
		else :
			voc = Voc(self)
			voc.build_voc()
			self.voc = voc.voc
		self.bow = []
		self.tdidf = []

	def lire (self) :
		return glob(self.corpus+"/*")

	def clean(self,ficstring) :
		ficstring = re.sub('(<[^>]*>)|\(|\)',' ',ficstring)
		ficstring = re.sub(' {2,}',' ',ficstring)
		return ficstring

	def string(self,fic) :

		return open(fic).read()

	def getBOW(self) :
		for fic in self.lire() :
			texte=re.sub('(<[^>]*>)|\(|\)',' ',self.string(fic))
			ligne=[]
			for mot in self.voc:
				regexp=re.compile(r'\b'+re.escape(mot)+r'\b') #prendre en compte frontieres de mots pour pas de résultats trop faussés
				if regexp.search(texte):
					ligne.append(1)
				else:
					ligne.append(0)
			self.bow.append(ligne)

	def getTFIDF(self) :
		for fic in self.lire() :
			texte= [str(item) for item in nlp(self.clean(self.string(fic))) if not item.is_space and not item.is_punct]
			ligne=[]
			for mot in self.voc:
				tf=texte.count(mot)/len(texte)
				regexp=re.compile(r'\b'+re.escape(mot)+r'\b')
				idf_part2=len([True for com in self.lire() if regexp.search(com)])#ex probleme avant lemmatisation : n't interprété comme mot à part par spacy mais du coup pas reconnu par notre regexp, donc ligne suivante pour régler le pb en attendant --> divison par 0 impossible, donc en attendant :
				if idf_part2==0:
					idf_part2=len([True for com in self.lire() if mot in com])
				idf=math.log2(len(self.lire())/idf_part2)
				ligne.append(tf*idf)

			self.tfidf.append(ligne)

		# print(self.bow)

class CorpusCSV(Corpus) :

	def __init__(self, path, voc = "") :
		self.corpus = path
		if voc :
			self.voc = voc
		else :
			voc = VocCSV(self)
			voc.build_voc()
			self.voc = voc.voc
			self.bigram=voc.bigram
			self.trigram=voc.trigram
		self.bow = []
		self.tfidf = []
	def string(self, fic) :
		return fic

	def lire(self):
		return self.corpus['text']




class Predict(object) :


	def __init__(self, doc, nlp, seuil = 0.5) :

		self.doc = doc
		self.seuil = seuil
		self.docnettoye = re.sub(r"<[^>]+>", " ", self.doc)
		self.nlp = nlp(self.docnettoye)


	def workspace(self) :

		self.tokens = []
		self.lemmas = []
		self.tag = []
		self.pos = []
		for token in self.nlp:
			if token.is_punct == False and token.is_space == False:
				self.tokens.append(token.text)
				self.lemmas.append(token.lemma_)
				self.tag.append(token.tag_)
				self.pos.append(token.pos_)

		for lemma in self.lemmas:
			n = self.lemmas.index(lemma)
			if lemma in ("interesting", "interested", "good", "recommended", "recommend" "excellent", "convincing", "thrilling", "satisfy", "amazing", "amazement", "beautiful", "delightful", "sublime", "great", "joyous", "fun", "funny", "legendary", "nice", "astounding", "enjoy", "fascinating", "fascinate", "remarkable", "memorable", "entertaining", "wonderful", "likable", "nifty", "favorite", "clever", "cleverly", "amusing", "gem", "chemistry", "masterpiece") or (lemma == "well" and n < len(self.lemmas)-1 and self.tag[n+1] == "VBN"):
				if "not" in (self.lemmas[n-3:n-1]) or "no" in (self.lemmas[n-3:n-1]) or "nothing" in (self.lemmas[n-3:n-1]) or "neither" in (self.lemmas[n-3:n-1]) or "nor" in (self.lemmas[n-3:n-1]) or "without" in (self.lemmas[n-3:n-1]) or "could" in (self.lemmas[n-5:n-2]) or "would" in (self.lemmas[n-5:n-2]) or "but" in (self.lemmas[n+1:n+4]) or "if" in (self.lemmas[n-5:n-2]):
					self.seuil -= 0.1
				else:
					self.seuil += 0.1
					if "so" in (self.lemmas[n-3:n-1]) or "truly" in (self.lemmas[n-3:n-1]) or "really" in (self.lemmas[n-3:n-1]) or "very" in (self.lemmas[n-3:n-1]) or "completely" in (self.lemmas[n-3:n-1]) or "highly" in (self.lemmas[n-3:n-1]) or "deeply" in (self.lemmas[n-3:n-1]):
						self.seuil += 0.1
					if self.tokens[n] == self.tokens[n].upper():
						self.seuil += 0.1

			elif (lemma in ("horrible", "lame", "despicable", "boring", "bored", "crap", "awful", "appalled", "scandalous", "sadly", "sad" "why", "how", "where" "failure", "fail", "ridiculous", "painful", "painfully", "horrendous", "disaster", "waste", "bad", "disappointed", "disappointment", "disappointing", "irritating" "pointless", "turgid", "emotionless", "embarrassed", "clichéd", "cliché" "stupid", "worthless", "bleak", "miscast", "weak", "problem", "incoherent", "unsuccessfull", "wooden", "annoying", "implausible", "overdone", "bizarre", "fake", "stereotype", "dangerous", "mediocrity", "mediocre", "dull", "terrible", "wrong", "empty", "silly", "poorly", "poor", "laughable", "pass", "hollow", "shallow", "message-less", "unfortunate", "inept", "unfunny", "deception", "pointlessly", "disastrous", "unnecessary", "unappealing", "goofy", "suck", "insane", "half-written", "pretentious", "unpleasant", "offensive", "feeble") and "not" not in (self.lemmas[n-3:n-1]) and "no" not in (self.lemmas[n-3:n-1]) and "nothing" not in (self.lemmas[n-3:n-1]) and "neither" not in (self.lemmas[n-3:n-1]) and "nor" not in (self.lemmas[n-3:n-1]) and "without" not in (self.lemmas[n-3:n-1])) or (lemma in ("plot", "development", "coherence") and ("without" in (self.lemmas[n-3:n-1]) or "no" in (self.lemmas[n-3:n-1])) or (lemma == "too" and n < len(self.lemmas)-1 and self.pos[n+1] == "ADJ")):
				self.seuil -= 0.1
				if "so" in (self.lemmas[n-3:n-1]) or "truly" in (self.lemmas[n-3:n-1]) or "really" in (self.lemmas[n-3:n-1]) or "very" in (self.lemmas[n-3:n-1]) or "completely" in (self.lemmas[n-3:n-1]) or "highly" in (self.lemmas[n-3:n-1]) or "deeply" in (self.lemmas[n-3:n-1]):
					self.seuil -= 0.1
				if self.tokens[n] == self.tokens[n].upper():
					self.seuil -= 0.1


		for token in self.tokens:
			n = self.tokens.index(token)
			if token == "worth" :
				try :
					if  self.tokens[n+1] == "watching" :
						if "not" in (self.tokens[n-3:n-1]):
							self.seuil  -= 0.5
						else:
							self.seuil  += 0.5
				except IndexError :
					print(self.tokens)
					print(self.tokens[n])


		if "unfortunately" in self.lemmas or "alas" in self.lemmas or "I wanted to like" in self.doc or "doesn't save this film" in self.doc or "don't go" in self.doc or "screwed up" in self.doc or "avoid watching" in self.doc or "avoid this film" in self.doc or "don't see it" in self.doc:
			self.seuil  -= 0.5
		elif "director should" in self.doc or "if only" in self.doc or "own risk" in self.doc or "look elsewhere" in self.doc:
			self.seuil -= 0.2



	def predict(self) :

		self.workspace()

		if self.seuil < 0.5 :
			self.predicted = 'neg'
		else :
			self.predicted = 'pos'


if __name__ == '__main__':

	c = Corpus('../../../imdb_test/neg')
	print(c.voc)
	c.getBOW()
	print(c.bow)
