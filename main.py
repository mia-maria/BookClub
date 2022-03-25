# Author: Mia-Maria Galistel, mg223tj
# Based on example code by Ilir Jusufi given in workshop.

# Represents the entry point of the application.

import mysql.connector
import database
import queries

# Establishes a connection to Mysql
# Substitute values for user, password and unix socket according to your settings.
cnx= mysql.connector.connect(user='root',
                             password='test',
                             #unix_socket= '/Applications/MAMP/tmp/mysql/mysql.sock',)
                             unix_socket= '/var/run/mysqld/mysqld.sock',)

cursor = cnx.cursor()

# Creates a database called BookClub if no such database already exists.
database.createDatabaseBookClub(cnx, cursor)


# Shows a main menu for the user. Executes queries and presents the results for the user depending on what the user wants to know.
def showMainMenu():
  response = input("Main menu: \n 1. List all books. \n 2. List all authors. \n 3. Get all books of an author. \n 4. Get a list with information about how the members have rated the books. \n 5. Get all books of a specific genre. \n 6. Get the average grades of the books. \n 7. Get the average grades for all authors based on their books. \n 8. Get information about which members that have read a certain book. \n Q. Quit \n --------- \n Please choose one option: ")

  def getInput():
      userInput = input("Return to main menu by pressing any key \n")
      if userInput == '':
        userInput = 'loggedKeystroke'
      return userInput

  if response == '1':
    queries.getAllBooks(cursor)
    if getInput():
      showMainMenu()
  if response == '2':
    queries.getAllAuthors(cursor)
    if getInput():
      showMainMenu()
  if response == '3':
    author = input("Enter author: ")
    queries.getBooksOfAuthor(cursor, author)
    if getInput():
      showMainMenu()
  if response == '4':
    queries.getGradedBooksByMembers(cursor)
    if getInput():
      showMainMenu()
  if response == '5':
    genre = input("Enter genre: ")
    queries.getBooksOfGenre(cursor, genre)
    if getInput():
      showMainMenu()
  if response == '6':
    queries.getAverageGradesOfBooks(cursor)
    if getInput():
      showMainMenu()
  if response == '7':
    queries.getAverageGradeForAuthor(cursor)
    if getInput():
      showMainMenu()
  if response == '8':
    book = input("Enter title: ")
    queries.getBook(cursor, book)
    if getInput():
      showMainMenu()

showMainMenu()

cursor.close()
cnx.close()