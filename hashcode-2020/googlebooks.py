import libreria
from parser import parser_library

def risolvi(n_libri: int, n_librerie: int, n_giorni: int, book_scores: [int], libraries: [libreria]):
    remaining_days = n_giorni
    OUTPUT_N_LIBS = 0
    OUTPUT_PACKS = []
    while len(libraries) > 0 and remaining_days > min([x.signup_time for x in libraries]):
        libraries = sorted(libraries, key=lambda x: x.calcola_potenziale(book_scores, remaining_days), reverse=True)
        best_lib = libraries.pop(0)
        books_to_send = best_lib.getSendableBooks(remaining_days)
        remaining_days -= best_lib.signup_time
        for x in books_to_send:
            book_scores[x] = 0
        OUTPUT_N_LIBS += 1
        OUTPUT_PACKS += [libreria.Pack(best_lib.ID, len(books_to_send), books_to_send)]
    return (OUTPUT_N_LIBS, OUTPUT_PACKS)


if __name__ == "__main__":
    # # parse
    # library1 = libreria.libreria(0, 5, 2, 2, [0,1,2,3,4])
    # library2 = libreria.libreria(1, 4, 3, 1, [3,2,5,0])
    # book_scores = [1,2,3,6,5,4]
    # libraries = [library1, library2]
    # tupla = risolvi(6, 2, 7, book_scores, libraries)
    # print(tupla[0])
    test = ["a_example.txt", "b_read_on.txt", "c_incunabula.txt", "d_tough_choices.txt", "e_so_many_books.txt", "f_libraries_of_the_world.txt"]
    i = 3
    a, b, c, d, e = parser_library(test[i])
    tupla = risolvi(a,b,c,d,e)

    str_risultato = str(tupla[0]) + "\n"
    for x in tupla[1]:
        str_risultato = str_risultato + str(x) + "\n"
    print(str_risultato)
    with open(test[i] + ".out", "w") as file:
        file.write(str_risultato)