from glob import glob
import re
import spacy
from spacy import displacy

#le Vocabulaire
class Voc(object) : 

	def __init__(self, parametre_corpus) :

		self.corpus = parametre_corpus #on doit préciser un corpus lors de l'appel du vocabulaire 
		self.voc = [] #on fait un vocabulire de mots à partir du corpus passé en paramètre
	#fonction utilisé dans l'exercice 1
	def build_voc(self) : #cette méthode crée un vocabulaire 
		self.voc = []
		#pour chaque fichier du corpus faire : 
		for fic in self.corpus.lire() :
             #on lit un fichier, on le nettoie et on remplace les saut de lignes par des espaces 
			ficstring = self.clean(self.corpus.string(fic).replace('\n',' '))
			#on divise le fichier en mots
			for mot in ficstring.split() :
                #éviter les doublons
				if mot not in self.voc :
                    #tous les mots qui ne se répetent pas sont ajoutés à la variable self.voc
					self.voc.append(mot)
		return self.voc #cette méthode renvoie une liste de mots qui constitue le vocabulaire du corpus passé en paramètre			
						
	def clean(self,ficstring) : #supprime les ponctuations, les balises br
		ficstring = ficstring.replace('(','')
		ficstring = ficstring.replace(')','')
		ficstring = ficstring.replace('<','')
		ficstring = ficstring.replace('>','')
		ficstring = ficstring.replace('/','')
		ficstring = ficstring.replace(':','')
		ficstring = ficstring.replace('"','')
		ficstring = ficstring.replace(',','')
		ficstring = ficstring.replace('!','')
		ficstring = ficstring.replace('?','')
		ficstring = ficstring.replace('.','')
		ficstring = ficstring.replace('--','')
		ficstring = ficstring.replace(';','')
		ficstring = ficstring.replace('/br','')
		ficstring = ficstring.replace('br','')
		ficstring = ficstring.replace('.br','')
		return ficstring

	def ecrire_voc(self,out) : 

		out.write('\n'.join([elem for elem in self.voc]))

	def load_voc(self, vocfile) : 

		self.voc = Voc.string(vocfile)
		
#le Corpus	
class Corpus(object) : 

	def __init__(self, path, voc = "") : #

		self.corpus = path
		if voc : #si le vocabulaire en présicé faire : 
			self.voc = Voc.load_voc(voc)
		else : #si le vocabulaire n'est pas précisé lors de l'appel de la classe Corpsu faire : 
			voc = Voc(self) 
			voc.build_voc()
			self.voc = voc.voc
		self.bow = []

	def lire (self) :
		return glob(self.corpus) #renvoie le nom des fichiers stockés dans un répértoire


	def string(self, fic) : 

		return open(fic).read() #renvoie le contenu du fichier passé en paramètre
   
	#fonction qui doit être utilisée dans l'exercice 2
	def getBOW(self) : 
		x = 0
		for fic in self.lire() :
                        pass
		 #cette fonction doit créer un sac des mots à partir des mots de notre corpus
	  	 #l'output doit être une liste de listes :  [[0,1,1,0,1],[1,0,1,1,1]] où les mots de notre corpus sont sous forme de 0 ou de 1
	  	 #0 si le mot d'un fichier ne fait pas partie du vocabulaire,  1 s'il y est  
         
			


if __name__ == '__main__':
        c=Corpus('./imdb/neg/*.txt') #appel de la classe Corpus
        voc=Voc(c) #appel de la classe Voc
        f=voc.build_voc() #appel la méthode de construiction d'un vocabulaire à partir du corpus passé en paramètre
        print(f)

"""
problèmes rencontrés : 
je n'ai pas compris qu'est-ce que veut dire :
		else :  
			voc = Voc(self) 
			voc.build_voc()
			self.voc = voc.voc
		self.bow = []
dans l'exercie 2, je n'ai pas su appeler le vocabulaire dans la fonction getBOW()
"""
