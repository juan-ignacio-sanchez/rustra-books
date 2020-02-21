import sys
from functools import reduce

used = set()
scores = []

class Library:

    def __init__(self, books, signup, books_per_day, index):
        self.books = books
        self.signup = signup
        self.books_per_day = books_per_day
        self.index = index
        self.books_to_send = []

    def score_per_book(self):
        return [(book, scores[book]) for book in self.books]

    def score_sum(self):
        scores_per_book = [scores[b] for b in self.books]
        return reduce(lambda x, y: x + y, scores_per_book)

    def rate(self):
        return (self.score_sum() / self.signup) * self.books_per_day

    def to_dict(self):
        return {'index': self.index, 'sent_books': len(self.books_to_send), 'booklist': self.books_to_send}

    def __str__(self):
        return f"SPB: {self.score_per_book()}, Rate: {self.rate()}, books: {self.books}, Signup: {self.signup}, PerDay: {self.books_per_day}"


def output(libs):
    ans = f'{len(libs)}\n'
    for lib in libs:
        ans += f'{lib["index"]} {lib["sent_books"]}\n'
        ans += ' '.join(lib['booklist'])
        ans += '\n'
    return ans


def scan(libraries, deadline):
    # sacar librerías hasta que la suma de su signup <= deadline
    total = 0
    to_send = []
    libraries = sorted(libraries, key=lambda x: x.rate(), reverse=True)

    while libraries and total <= deadline:
        lib, tail = libraries[0], libraries[1:]
        libraries = tail
        libraries = sorted(libraries, key=lambda x: x.rate(), reverse=True)
        libraries = [lib for lib in libraries if lib.signup + total < deadline]
        total += lib.signup
        if total <= deadline:
            # select books
            total_books_to_choose = min(len(lib.books), lib.books_per_day * (deadline - total))
            lib.books_to_send = [str(x[0]) for x in sorted(lib.score_per_book(), key=lambda x: x[1], reverse=True)[:total_books_to_choose]]
            for book in lib.books_to_send:
                scores[int(book)] = 0
            to_send.append(lib.to_dict())

    # for lib in libraries:
    #     total += lib.signup
    #     if total <= deadline:
    #         # select books
    #         total_books_to_choose = min(len(lib.books), lib.books_per_day * (deadline - total))
    #         lib.books_to_send = [str(x[0]) for x in sorted(lib.score_per_book(), key=lambda x: x[1], reverse=True)[:total_books_to_choose]]
    #         for book in lib.books_to_send:
    #             scores[int(book)] = 0
    #         to_send.append(lib.to_dict())
    #     else:
    #         break
    return to_send


def main(path):
    global scores
    with open(path, 'r') as data:
        total_books, total_libraries, deadline = [int(x) for x in data.readline()[:-1].split(' ')]
        scores = [int(x) for x in data.readline()[:-1].split(' ')]
        libraries = []
        libs = data.readlines()
        index = 0
        for lib in range(0, len(libs), 2):
            _, signup, books_per_day = [int(x) for x in libs[lib][:-1].split(' ')]
            books = [int(x) for x in libs[lib+1][:-1].split(' ')]
            libraries.append(Library(books, signup, books_per_day, index=index))
            index += 1

        # print([print(l) for l in libraries])
        out = output(scan(libraries, deadline))
        print(out)


if __name__ == '__main__':
    main(sys.argv[1])