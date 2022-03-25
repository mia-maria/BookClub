# Author: Mia-Maria Galistel, mg223tj
# Based on example code by Ilir Jusufi given in workshop.

# Represents a database module.

import mysql.connector
from mysql.connector import errorcode
import csv

DB_NAME = 'BookClub'

# Creates a database.
def create_database(cursor, DB_NAME):
    try:
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed to create a database {}".format(err))
        exit(1)

# Create a table named authors if it doesn't exist.
def create_table_authors(cursor):
  create_authors = "CREATE TABLE `authors` (" \
                 "  `name` varchar(40) NOT NULL," \
                 "  `birth_year` SMALLINT NOT NULL," \
                 "  `country` varchar(50) NOT NULL," \
                 "  PRIMARY KEY (`name`)" \
                 ") ENGINE=InnoDB"
  try:
            print("Creating table authors: ")
            cursor.execute(create_authors)
  except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print("Table authors already exists.")
            else:
                print(err.msg)
  else:
          print("OK")

# Create a table named members if it doesn't exist.
def create_table_members(cursor):
  create_members = "CREATE TABLE `members` (" \
                 "  `name` varchar(40) NOT NULL," \
                 "  `social_security_number` varchar(11) NOT NULL," \
                 "  `location` varchar(20) NOT NULL," \
                 "  PRIMARY KEY (`social_security_number`)" \
                 ") ENGINE=InnoDB"
  try:
            print("Creating table members: ")
            cursor.execute(create_members)
  except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print("Table members already exists.")
            else:
                print(err.msg)
  else:
          print("OK")

# Create a table named books if it doesn't exist.
def create_table_books(cursor):
  create_books = "CREATE TABLE `books` (" \
                 "  `title` varchar(120) NOT NULL," \
                 "  `author` varchar(40) NOT NULL," \
                 "  `genre` varchar(25) NOT NULL," \
                 "  PRIMARY KEY (`title`)," \
                 "  FOREIGN KEY (`author`) REFERENCES authors(name)" \
                 ") ENGINE=InnoDB"
  try:
            print("Creating table books: ")
            cursor.execute(create_books)
  except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print("Table books already exists.")
            else:
                print(err.msg)
  else:
          print("OK")

# Create a table named graded books if it doesn't exist.
def create_table_gradedBooks(cursor):
  create_gradedBooks = "CREATE TABLE `graded_books` (" \
                 "  `member` varchar(11) NOT NULL," \
                 "  `title` varchar(120) NOT NULL," \
                 "  `grade` SMALLINT NOT NULL," \
                 "  CONSTRAINT graded_book PRIMARY KEY (`member`, `title`)" \
                 ") ENGINE=InnoDB"
  try:
            print("Creating table graded books: ")
            cursor.execute(create_gradedBooks)
  except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print("Table graded books already exists.")
            else:
                print(err.msg)
  else:
          print("OK")

# Add values to the table authors.
def insert_into_authors(cnx, cursor):
  file = "authors.csv"
  insert_sql = "INSERT INTO authors (name, birth_year, country) VALUES (%s, %s, %s)"
  insert_into_table(cnx, cursor, file, insert_sql)

# Add values to the table members.
def insert_into_members(cnx, cursor):
  file = "members.csv"
  insert_sql = "INSERT INTO members (name, social_security_number, location) VALUES (%s, %s, %s)"
  insert_into_table(cnx, cursor, file, insert_sql)

# Add values to the table book details.
def insert_into_books(cnx, cursor):
  file = "books.csv"
  insert_sql = "INSERT INTO books (title, author, genre) VALUES (%s, %s, %s)"
  insert_into_table(cnx, cursor, file, insert_sql)

# Add values to the table graded books.
def insert_into_gradedBooks(cnx, cursor):
  file = "gradedBooks.csv"
  insert_sql = "INSERT INTO graded_books (member, title, grade) VALUES (%s, %s, %s)"
  insert_into_table(cnx, cursor, file, insert_sql)


# Add values to a table.
def insert_into_table(cnx, cursor, file, insert_sql):
  file = open(file, encoding="utf8")
  parser = csv.reader(file)
  rows = []
  rowCounter = 0
  for row in parser:
    # Rows are added to the table (the column names are skipped).
    if rowCounter != 0:
      passed = True
      for value in row:
        if value == 'NA':
          passed = False
      if passed:
        rows.append(row)
    rowCounter += 1
  file.close()
  try:
    cursor.executemany(insert_sql, rows)
  except mysql.connector.Error as err:
      print(err.msg)
  else:
      # Commits data.
      cnx.commit()
      print("OK")

# Creates a view about the average grades for all authors based on their books.
def createAuthorView(cursor):
  createView = "CREATE VIEW author_view as SELECT books.author, AVG(graded_books.grade) as 'average grade' FROM graded_books INNER JOIN books ON graded_books.title = books.title GROUP BY author ORDER BY author;"
  cursor.execute(createView)

# Creates a database named BookClub, if there isn't one already.
def createDatabaseBookClub(cnx, cursor):
  try:
    cursor.execute("USE {}".format(DB_NAME))
  except mysql.connector.Error as err:
    print("Database {} does not exist".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor, DB_NAME)
        print("Database {} created succesfully.".format(DB_NAME))
        cnx.database = DB_NAME
        # Creates tables.
        create_table_authors(cursor)
        create_table_members(cursor)
        create_table_books(cursor)
        create_table_gradedBooks(cursor)
        # Inserts data to the tables.
        insert_into_authors(cnx, cursor)
        insert_into_members(cnx, cursor)
        insert_into_books(cnx, cursor)
        insert_into_gradedBooks(cnx, cursor)
        # Creates a view
        createAuthorView(cursor)

    else:
        print(err)
