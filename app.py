from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    page = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    publication = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Book %r>' % self.id


# class users(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.Text, nullable=False)
#     email = db.Column(db.Text, nullable=False)
#     psw = db.Column(db.Text, nullable=False)
#     time = db.Column(db.DateTime, default=datetime.utcnow)
#
#     def __repr__(self):
#         return '<users %r>' % self.id_id


@app.route('/')
@app.route('/home')
def index():  # put application's code here

    return render_template('index.html')


@app.route('/books-page')
def books_page():  # put application's code here
    books = Book.query.order_by(Book.date).all()
    return render_template('books-page.html', books=books)


@app.route('/books-detail/<int:id>')
def books_detail(id):
    book = Book.query.get(id)
    return render_template("books_detail.html", book=book)


@app.route('/about')
def about():  # put application's code here
    return render_template('about.html')


@app.route('/create-book', methods=('POST', 'GET'))
def create_book():  # put application's code here
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        page = request.form['page']
        text = request.form['text']
        publication = request.form['publication']
        book = Book(title=title, author=author, page=page, text=text, publication=publication)
        try:
            db.session.add(book)
            db.session.commit()
            return redirect('/books-page')
        except:
            return "При добовлении статьи произошла ошибка!"
    else:
        return render_template('create-book.html')


@app.route('/books/<int:id>/delete')
def book_delete(id):
    book = Book.query.get_or_404(id)

    try:
        db.session.delete(book)
        db.session.commit()
        return redirect('/books-page')
    except:
        return "При удалении статьи произошла ошибка!"


@app.route('/books/<int:id>/update', methods=['POST', 'GET'])
def book_update(id):
    book = Book.query.get_or_404(id)
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.page = request.form['page']
        book.text = request.form['text']
        book.publication = request.form['publication']
        try:
            db.session.commit()
            return redirect('/books-page')
        except:
            return "При редоктировании статьи произошла ошибка!"
    else:

        return render_template('books_update.html', book=book)


@app.route('/login')
def login():  # put application's code here
    return render_template('login.html')


@app.route('/register')
def register():  # put application's code here
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)
