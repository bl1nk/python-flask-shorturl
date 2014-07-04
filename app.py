#!/usr/bin/env python
import os
import sqlite3
from string import letters, digits
from random import choice
from urlparse import urlsplit
from flask import Flask, request, g, render_template, redirect, url_for, flash
app = Flask(__name__)

# db {{{

db_file = os.path.join(app.root_path, 'purl.db')

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def connect_db():
    rv = sqlite3.connect(db_file)
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

# }}}
# routes {{{

@app.route('/', methods=['GET', 'POST'])
def hi():
    url = None
    if request.method == 'POST':
        value = request.form['url']
        if validate_url(value):
            url = insert_url(value)
    return render_template('new.html', url=url)

@app.route('/<shorturl>')
def get_url(shorturl):
    db = get_db()
    url = db.execute('select url from entries where hash=(?)', (shorturl,))
    return redirect(url.fetchone()[0])

@app.route('/favicon.ico/')
def do_not_serve():
    return ''

# }}}
# helper methods {{{

def insert_url(url):
    shorturl = generate_hash()
    db = get_db()
    db.execute('insert into entries (hash,url) values (?,?)', [shorturl,url])
    db.commit()
    return request.url + shorturl

def generate_hash(chars=letters+digits, r=6):
    return ''.join(choice(chars) for i in range(r))

def validate_url(url):
    o = urlsplit(url)
    return o.scheme in ('http','https') and '.' in o.netloc

# }}}

if __name__ == "__main__":
    app.run(debug=True)
