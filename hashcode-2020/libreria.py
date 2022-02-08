class libreria:
    def __init__(self, ID: int, n_libri: int, signup_time: int, books_per_day: int, books: list):
        self.ID = ID
        self.n_libri = n_libri
        self.signup_time = signup_time
        self.books_per_day = books_per_day
        self.books = books
        self.must_sort = not (min(self.books) == max(self.books))
    
    def calcola_potenziale(self, book_scores, remaining_days) -> int:
        # Chiamare questa funzione ordina in-place self.books in ordine decrescente
        days = remaining_days - self.signup_time
        n_books_sendable = days * self.books_per_day
        if self.must_sort:
            self.books = sorted(self.books, key=lambda x:book_scores[x], reverse=True)
        return sum([book_scores[x] for x in self.books[:min(len(self.books),n_books_sendable+1)]])

    def getSendableBooks(self, remaining_days):
        days = remaining_days - self.signup_time
        n_books_sendable = days * self.books_per_day
        return self.books[:min(len(self.books),n_books_sendable+1)]

    def __str__(self):
        return str(self.ID)

class Pack:
    def __init__(self, lib_ID: int, n_books: int, books: [int]):
        self.lib_ID = lib_ID
        self.n_books = n_books
        self.books = books

    def __str__(self):
        books = ""
        for x in self.books:
            books += str(x) + " "
        books = books[:-1]
        return str(self.lib_ID) + " " + str(self.n_books) + "\n" + books

if __name__ == "__main__":
    library = libreria(0, 5, 2, 2, [0,1,2,3,4])
    book_scores = [1,2,3,6,5,4]
    print(library.calcola_potenziale(book_scores,7))