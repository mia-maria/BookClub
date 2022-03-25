# Author: Mia-Maria Galistel, mg223tj
# Based on example code by Ilir Jusufi given in workshop.

# Represents a queries module.


# List the author, title and genre of the books ordered by the authors.
def getAllBooks(cursor):
  getBooksQuery = "SELECT author, title, genre FROM books ORDER BY author;"
  cursor.execute(getBooksQuery)

  print("\n\n")
  print("| {:<22} |{:<45} | {}".format("author", "title", "genre"))
  print("-"*95)
  for (author, title, genre) in cursor:
      print("| {:<22} |{:<45} | {}".format(author, title, genre))
  
  print("\n\n")


# List name, birth year and country of the authors.
def getAllAuthors(cursor):
  getAuthorsQuery = "SELECT * FROM authors;"
  cursor.execute(getAuthorsQuery)

  print("\n\n")
  print("| {:<22} |{:<10} | {}".format("author", "birth year", "country"))
  print("-"*60)
  for (author, birth_year, country) in cursor:
      print("| {:<22} |{:<10} | {}".format(author, birth_year, country))
  
  print("\n\n")


# List title and genre of all books of a specific author.
def getBooksOfAuthor(cursor, author):
  bookQuery = "SELECT books.title, books.genre FROM books INNER JOIN authors ON books.author = authors.name WHERE books.author = %s;"
  requestedAuthor = list(author.split(","))
  cursor.execute(bookQuery, requestedAuthor)

  print("\n\n")
  print("Books by " + author + "\n")
  print("| {:<45} |{:<20} ".format("title", "genre"))
  print("-"*65)
  for (title, genre) in cursor:
      print("| {:<45} |{:<20} ".format(title, genre))
  
  print("\n")
  count = cursor.rowcount
  if count == 0:
    print("There is no information about author " + author + " in the database.")
    print("\n\n")


# List member, title, author and grade of all graded books by the members.
def getGradedBooksByMembers(cursor):
  booksQuery = "SELECT members.name, graded_books.title, books.author, graded_books.grade FROM graded_books INNER JOIN books ON graded_books.title = books.title INNER JOIN members ON graded_books.member = members.social_security_number;"
  cursor.execute(booksQuery)

  print("\n\n")
  print("| {:<20} | {:<44} |{:<20} | {}".format("member", "title", "author", "grade"))
  print("-"*100)
  for (member, title, author, grade) in cursor:
      print("| {:<20} |{:<45} |{:<20} | {}".format(member, title, author, grade))
  
  print("\n\n")


# List title, author and genre of a specific genre from the table books given a genre.
def getBooksOfGenre(cursor, genre):
  genreQuery = "SELECT * FROM books WHERE genre = %s;"
  requestedGenre = list(genre.split(","))
  cursor.execute(genreQuery, requestedGenre)

  print("\n\n")
  print("| {:<45} |{:<22} |{:<20} ".format("title", "author", "genre"))
  print("-"*90)
  for (title, author, genre) in cursor:
      print("| {:<45} |{:<22} |{:<20}".format(title, author, genre))
  
  print("\n")
  count = cursor.rowcount
  if count == 0:
    print("There are no books in the genre " + genre + " in the database.")
    print("\n\n")


# List title, author and average grade of all the graded books.
def getAverageGradesOfBooks(cursor):
  averageQuery = "SELECT graded_books.title, books.author, AVG(graded_books.grade) FROM graded_books INNER JOIN books ON graded_books.title = books.title GROUP BY title ORDER BY title;"
  cursor.execute(averageQuery)

  print("\n\n")
  print("| {:<50} |{:<25} | {}".format("title", "author", "average grade"))
  print("-"*95)
  for (title, author, grade) in cursor:
      print("| {:<50} |{:<25} | {}".format(title, author, grade))
  
  print("\n\n")


# Provides information about the names and the average grades for all authors based on their books.
def getAverageGradeForAuthor(cursor):
  getAverageQuery = "SELECT * FROM author_view;"
  cursor.execute(getAverageQuery)

  print("\n\n")
  print("| {:<25} | {}".format("author", "average grade"))
  print("-"*95)
  for (author, grade) in cursor:
      print("| {:<25} | {}".format(author, grade))
  
  print("\n\n")


# Provides information about a given title, the members that have read this book and their location.
def getBook(cursor, book):
  bookQuery = "SELECT graded_books.title, members.name, members.location FROM graded_books INNER JOIN members ON graded_books.member = members.social_security_number WHERE title = %s ORDER BY members.name;"
  title = list(book.split(","))
  cursor.execute(bookQuery, title)

  print("\n\n")
  print("| {:<45} |{:<22} | {}".format("title", "member", "location"))
  print("-"*90)
  for (title, member, location) in cursor:
      print("| {:<45} |{:<22} | {}".format(title, member, location))
  
  print("\n")
  count = cursor.rowcount
  if count == 0:
    print("\n\n")
    print("The title " + book + " does not exist.")
    print("\n\n")


