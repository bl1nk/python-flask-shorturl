#!/usr/bin/env python
import os
import sqlite3
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

@app.route("/")
def index():
    return redirect(url_for('new_url'))

@app.route("/new")
def new_url():
    return "ok"

def create_url():
    return "yep"

# }}}

if __name__ == "__main__":
    app.run(debug=True)
