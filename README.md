# CSCI-320-Books-Database
Principles of Data Management CSCI 320 Books Domain Database Project

# Dependency Installation
pip install -r requirements.txt

# Libraries
python-dotenv  
sshtunnel  
psycopg2-binary  
sqlalchemy  

# Contributors
clh5602 - Colby Heaton  
rto9185 - Ryan Ong  
gps5307 - Galen Sagarin  
alf9310 - Audrey Fuller  
tgk1703 - Thalia Kennedy

# Project Requirements
For the project:  
Users will be able to create new accounts and access via login. The system must record the date and time an account is created. It must also store the dates and times users access the application  
- Users will be able to create collections of books.
- Users will be to see the list of all their collections by name in ascending order. The list  must show the following information per collection:
  - Collections name
  - Number of books in the collection
  - Total length of the books (in pages) in the collection
  - Users will be able to search for books by name, release date, authors, publisher, or
  - genre. The resulting list of books must show the books name, the authors, the pub-
lisher, the length, audience and the ratings. The list must be sorted alphabetically
(ascending) by books name and release date. Users can sort the resulting list: book
name, publisher, genre, and released year (ascending and descending).

- Users can add and delete books from their collection.
- Users can modify the name of a collection. They can also delete an entire collection
- Users can rate a books (star rating)
- Users can read a book by selecting the starting and ending pages from a particular
book or they can read a random book from a collection. You must record every time
a book is read by a user. You do not need to actually be able to read books, simply
mark them as read.
- Users can follow another user. Users can search for new users to follow by email
- The application must also allow an user to unfollow a another user
