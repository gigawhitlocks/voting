from flask import (Flask,
                   escape,
                   flash,
                   g,
                   redirect,
                   render_template,
                   request,
                   session,
                   url_for)
import flask_login

from wtforms import (PasswordField,
                     SubmitField,
                     TextField,
                     validators,
                     Form)

import uuid
import math
import os.path
import os
import requests
import sqlite3

app = Flask(__name__)
app.secret_key = os.getenv('BOOKCLUB_SECRET_KEY')
if not app.secret_key:
    exit("Please set environment variable BOOKCLUB_SECRET_KEY to a long secret string")

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
users={}

DATABASE = 'database.db'

class User(flask_login.UserMixin):
    id = u""
    def get_id(self):
        return self.id

@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return

    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if username not in users:
        return

    user = User()
    user.id = username
    return user

class LoginForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password')
    submit = SubmitField()

class AddBookForm(Form):
    author = TextField('Author')
    title = TextField('Title')
    link = TextField('Goodreads/Wiki/Amazon Link')
    description = TextField('Displayed text for link above')
    submit = SubmitField()

@app.route('/add', methods=['GET', 'POST'])
@flask_login.login_required
def addbook():
    if request.method == 'POST':
        cur = get_db()
        query = '''
        INSERT INTO books (title, author, link, description, id)
        VALUES(?, ?, ?, ?, ?);'''

        cur.execute(query,
                    (request.form.get('title',''),
                     request.form.get('author',''),
                     request.form.get('link',''),
                     request.form.get('description',''),
                     uuid.uuid4().hex))
        cur.commit()
        cur.close()
        return redirect(url_for('index'))

    form = AddBookForm()
    return render_template('add_book.html',
                            form=form,
                            splash=url_for('static', filename='books.jpg'))

def authenticate(request):
    r = requests.post("https://shouting.online/api/v1/login",
                        headers={"content-type":"application/json"},
                        json={"username":request.form['username'],
                            "password":request.form['password']})

    return r.status_code == 200

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/vote',methods=['POST', 'GET'])
@flask_login.login_required
def vote():
    if request.method == 'POST' :

        cur = get_db()
        for vote in request.form :
            points = request.form["{}".format(vote)]
            if points:
                query = '''DELETE FROM votes WHERE name=? AND id=?;'''
                cur.execute(query, (flask_login.current_user.id, vote))
                query = '''INSERT INTO votes VALUES(?, ?, ?);'''
                cur.execute(query, (flask_login.current_user.id, points, vote))

        cur.commit()
        cur.close()

    return redirect(url_for('index'))

@app.route('/')
def index():
    if not flask_login.current_user.is_authenticated:
        return redirect(url_for('login'))

    rows = query_db("SELECT * FROM books")
    books = []
    for row in rows:
        books.append({
            "id": row['id'],
            "title": row['title'],
            "author": row['author'],
            "link": row['link'],
            "description": row['description'],
            "score": 0
        })

    for book in books:
         row = query_db('''
            SELECT sum(points) FROM votes WHERE id='{0}';
            '''.format(book['id']))

         for r in row[0]:
             if r is not None:
                 book['score'] = r

    books = sorted(books, key=lambda x: -1*x['score'])
    return render_template('index.html',
                           books=books,
                           user=flask_login.current_user.id,
                           splash=url_for('static', filename='books.jpg'))


@app.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return "logged out"

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' :
        if authenticate(request):
            username = request.form['username']
            user = User()
            user.id = username
            users[username] = True
            flask_login.login_user(user)
            return redirect(url_for('index'))

    return render_template('login.html',
                            form=form,
                            splash=url_for('static', filename='books.jpg'))

if __name__ == "__main__":
    if not os.path.isfile(DATABASE):
        init_db()
    app.run(host='0.0.0.0')
