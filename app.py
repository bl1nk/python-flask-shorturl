#!/usr/bin/env python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hi():
    return "hello"

if __name__ == "__main__":
    app.run(debug=True)
