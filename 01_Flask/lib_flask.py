from flask import Flask, render_template, request
from psycopg2 import OperationalError, connect
from models import Book, Client
from datetime import date, timedelta


USER = "postgres"
HOST = "localhost"
PASSWORD = "coderslab"
today = date.today()


def execute_sql(sql, db):
    try:
        cnx = connect(user=USER, password=PASSWORD, host=HOST, database=db)
        cnx.autocommit = True
        cursor = cnx.cursor()
        cursor.execute(sql)
        if cursor.rowcount > 0:
            result = []
            for row in cursor:
                result.append(row)
            return result
    except OperationalError as e:
        return f"Coś poszło nie tak, napotkano błąd: {e}."
    else:
        cursor.close()
        cnx.close()


def execute_sql_fetchall(sql, db):
    try:
        cnx = connect(user=USER, password=PASSWORD, host=HOST, database=db)
        cnx.autocommit = True
        cursor = cnx.cursor()
        cursor.execute(sql)
        if cursor.rowcount > 0:
            result = []
            for row in cursor.fetchall():
                result.append(row)
            return result
    except OperationalError as e:
        return f"Coś poszło nie tak, napotkano błąd: {e}."
    else:
        cursor.close()
        cnx.close()


def execute_sql_insert(sql, db):
    try:
        cnx = connect(user=USER, password=PASSWORD, host=HOST, database=db)
        cnx.autocommit = True
        cursor = cnx.cursor()
        cursor.execute(sql)
        pass
    except OperationalError as e:
        return f"Coś poszło nie tak, napotkano błąd: {e}."
    else:
        cursor.close()
        cnx.close()


app = Flask(__name__)


@app.route('/')
def index():
    return "Welcome to your the most powerful library site!"


@app.route('/books')
def show_books():
    sql = "select * from book"
    books = execute_sql(sql, 'library_db')
    html = ""
    for book in books:
        html += f"{book[0]}; {book[1]}; {book[2]}; {book[3]}; {book[4]}; {book[5]}<br>"
    return html


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'GET':
        return render_template('book_form.html')
    elif request.method == 'POST':
        isbn = request.form.get('isbn', '')
        name = request.form.get('name', '')
        desc = request.form.get('desc', '')
        author_id = request.form.get('author_id', '')
        if isbn != '' and name != '' and desc != '' and author_id != '':
            sql = f"""insert into book(isbn, name, description, author_id)
                     values('{isbn}', '{name}', '{desc}', '{author_id}')"""
            execute_sql_insert(sql, 'library_db')
            return "Udało się dodać nową książkę."
        return "Nie udało się dodać nowej książki."
    else:
        return "Nieznana metoda."


@app.route('/book_details/<id>')
def books_details(id):
    sql = f"""select * from book where id='{id}'"""
    result = execute_sql(sql, "library_db")
    book = result[0]
    return f"""
    ID: {book[0]}<br>
    ISBN: {book[1]}<br>
    Title: {book[2]}<br>
    Description: {book[3]}<br>
    Is loaned: {book[4]}<br>
    Author ID: {book[5]}<br>
    """


@app.route('/delete_book/<book_id>')
def delete_book(book_id):
    sql = f"""select * from book where id='{book_id}'"""
    result = execute_sql(sql, "library_db")
    try:
        book = result[0]
    except TypeError:
        return "Nie ma książki o takim ID."
    sql2 = f"""delete from book where id='{book_id}'"""
    result = execute_sql_insert(sql2, "library_db")
    return f"Usunięto książkę o ID {book_id}."


@app.route('/clients')
def show_clients():
    sql = f"""select * from client"""
    clients = execute_sql(sql, "library_db")
    result = ""
    for client in clients:
        result += f"{client[0]}; {client[1]}; {client[2]}<br>"
    return result


@app.route('/add_client', methods=['GET', 'POST'])
def add_client():
    if request.method == "GET":
        return render_template('client_form.html')
    elif request.method == "POST":
        name = request.form.get("name", '')
        surname = request.form.get("last_name", '')
        sql = f"""insert into client(first_name, last_name) values('{name}', '{surname}')"""
        result = execute_sql_insert(sql, "library_db")
        return "Dodano klienta."
    else:
        return "Coś poszło nie tak."

execute_sql
@app.route('/delete_client/<client_id>')
def delete_client(client_id):
    sql = f"""select * from client where id='{client_id}'"""
    result = execute_sql(sql, "library_db")
    try:
        client = result[0]
    except TypeError:
        return f"Użytkownik o id {client_id} nie istnieje."
    sql = f"""delete from client where id='{client_id}'"""
    result = execute_sql_insert(sql, "library_db")
    return f"Usunięto użytkownika o ID: {client_id}."


@app.route('/client_details/<client_id>')
def show_client_details(client_id):
    sql = f"""select * from client join clients_books on client.id = clients_books.client_id where client.id='{client_id}'"""
    result = execute_sql(sql, "library_db")
    client = result[0]
    return f"""
    ID: {client[0]}<br>
    Imię: {client[1]}<br>
    Nazwisko: {client[2]}<br>
    ID książki: {client[5]}<br>
    """


@app.route('/loan', methods=['GET', 'POST'])
def loan_a_book():
    if request.method == 'GET':
        # part with clients select
        valid_clients = f"""select * from client"""
        result = execute_sql_fetchall(valid_clients, "library_db")
        clients = []
        for row in result:
            id_, first_name, second_name = row
            client = Client(first_name, second_name)
            client._id = id_
            client._full_name = first_name + " " + second_name
            clients.append(client)
        # part with books select
        available_books_sql = f"""select * from book where is_loaned=FALSE"""
        result = execute_sql_fetchall(available_books_sql, "library_db")
        books = []
        try:
            for row in result:
                id_, isbn, name, description, is_loaned, author_id = row
                book = Book(isbn, name, description, is_loaned, author_id)
                book._id = id_
                books.append(book)
            return render_template('loan_template.html', books=books, clients=clients)
        except TypeError:
            return """Brak książek do wypożyczenia.
            <html>
                <br>
                <a href="/loan">Wróć</a>
            </html>
            """
    elif request.method == 'POST':
        book_id = request.form.get('selected_book')
        client_id = request.form.get('selected_client')
        if book_id and client_id:
            execute_sql_insert(f"update book set is_loaned=TRUE where id={book_id}", "library_db")
            execute_sql_insert(f"insert into clients_books(client_id, book_id, loan_date, return_date) values('{client_id}', '{book_id}', '{today}', '{today+ timedelta(30)}')", "library_db")
            return """Udało się wypożyczyć książkę.
            <html>
                <br>
                <a href="/loan">Wróć</a>
            </html>
            """
        else:
            return """Cos poszło nie tak.
            <html>
                <br>
                <a href="/loan">Wróć</a>
            </html>
            """
    else:
        return """Coś poszło nie tak.
        <html>
            <br>
            <a href="/loan">Wróć</a>
        </html>
        """


if __name__ == "__main__":
    app.run(debug=True)
