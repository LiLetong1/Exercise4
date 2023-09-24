import sqlite3

DATABASE_NAME = 'library.db'

def connect_to_db():
    return sqlite3.connect(DATABASE_NAME)

def execute_db_query(query, params=()):
    with connect_to_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor

def create_tables():
    execute_db_query('''CREATE TABLE IF NOT EXISTS Books
                        (BookID TEXT PRIMARY KEY, Title TEXT, Author TEXT, ISBN TEXT, Status TEXT)''')
    execute_db_query('''CREATE TABLE IF NOT EXISTS Users
                        (UserID TEXT PRIMARY KEY, Name TEXT, Email TEXT)''')
    execute_db_query('''CREATE TABLE IF NOT EXISTS Reservations
                        (ReservationID TEXT PRIMARY KEY, BookID TEXT, UserID TEXT, ReservationDate TEXT)''')

def add_book(book_id, title, author, isbn, status):
    execute_db_query("INSERT INTO Books VALUES (?, ?, ?, ?, ?)", (book_id, title, author, isbn, status))

def find_book_by_id(book_id):
    cursor = execute_db_query('''SELECT Books.*, Users.Name, Users.Email, Reservations.ReservationDate 
                                FROM Books 
                                LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                                LEFT JOIN Users ON Reservations.UserID = Users.UserID
                                WHERE Books.BookID = ?''', (book_id,))
    return cursor.fetchone()

def find_books():
    cursor = execute_db_query('''SELECT Books.*, Users.Name, Users.Email, Reservations.ReservationDate 
                                FROM Books 
                                LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                                LEFT JOIN Users ON Reservations.UserID = Users.UserID''')
    return cursor.fetchall()

def update_book(book_id, title=None, author=None, isbn=None, status=None):
    params = (title, author, isbn, book_id)
    execute_db_query('''UPDATE Books SET Title=?, Author=?, ISBN=? WHERE BookID=?''', params)

    if status:
        execute_db_query("UPDATE Books SET Status=? WHERE BookID=?", (status, book_id))
        # (Additional logic for Reservations table can be added here if needed)

def delete_book(book_id):
    execute_db_query("DELETE FROM Reservations WHERE BookID=?", (book_id,))
    execute_db_query("DELETE FROM Books WHERE BookID=?", (book_id,))

def main():
    create_tables()
    actions = ['Add new books', 'Find book details based on BookID', 'Find all books', 'Update the book details', 'Delete books', 'Quit']

    while True:
        for idx, action in enumerate(actions, 1):
            print(f"{idx}. {action}")

        choice = input('Please select an action: ')

        try:
            if choice == '1':
                details = (input("Please enter BookID: "),
                           input("Please enter the title: "),
                           input("Please enter author: "),
                           input("Please enter ISBN: "),
                           input("Please enter the status (available or reserved): "))
                add_book(*details)
                print("Book added successfully!")
            elif choice == '2':
                book = find_book_by_id(input("Please enter BookID: "))
                if book:
                    print(book)
                else:
                    print("Book not found!")
            elif choice == '3':
                for book in find_books():
                    print(book)
            elif choice == '4':
                book_id = input("Please enter BookID: ")
                title = input("Please enter a new title or leave it blank: ")
                author = input("Please enter a new author or leave blank: ")
                isbn = input("Please enter a new ISBN or leave it blank: ")
                status = input("Please enter a new status or leave it blank (available or reserved): ")
                update_book(book_id, title, author, isbn, status)
                print("Book updated successfully!")
            elif choice == '5':
                delete_book(input("Please enter BookID: "))
                print("Book deleted successfully!")
            elif choice == '6':
                break
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
