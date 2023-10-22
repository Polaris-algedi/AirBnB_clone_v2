#!/usr/bin/python3
"""Script that starts a Flask web application"""
from flask import Flask
from html import escape

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """Route to display 'Hello HBNB!'"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Route to display 'HBNB'"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_text(text):
    """Route to display 'C text'"""
    text = text.replace('_', ' ')
    return f"C {escape(text)}"


@app.route("/python/", defaults={'text': 'is_cool'}, strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_text(text):
    """Route to display the default 'Python is cool' or 'Python text'"""
    text = text.replace('_', ' ')
    return f"Python {escape(text)}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
