import libreria
def parsify(fileName):
	with open(fileName, 'r') as f:
		lines = f.read().splitlines()
		#prima linea
		libris = int(lines[0].split()[0])
		librerie = int(lines[0].split()[1])
		giorni = int(lines[0].split()[2])
		

		punteggio_libri_linea = lines[1].split()
		punteggio_libri = [ int(x) for x in punteggio_libri_linea ]
	return(libris,librerie,giorni,punteggio_libri)

def parsify_libreria(fileName):
	with open(fileName, 'r') as f:
		lines = f.read().splitlines()
		id_libreria = 0
		lista_librerie = []
		for counter in range(2,len(lines)-1, 2):
				n_libri = int(lines[counter].split()[0])
				tempo_signup = int(lines[counter].split()[1])
				books_per_day = int(lines[counter].split()[2])
				books = [int(x) for x in lines[counter+1].split()]
				newLib = libreria.libreria(id_libreria, n_libri,tempo_signup,books_per_day,books)
				id_libreria += 1
				lista_librerie += [newLib]
		return(lista_librerie)

def parser_library(fileName):
	a = parsify(fileName)
	b = parsify_libreria(fileName)
	return(a[0],a[1],a[2],a[3],b)

if __name__ == '__main__':
	fileName = 'test.in'
	#test
#print(parsify(fileName))
	print(parser_library(fileName))