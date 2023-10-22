#!/usr/bin/python3
"""Script that starts a Flask web application"""
from flask import Flask
from html import escape
from flask import render_template

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


@app.route("/number/<int:n>", strict_slashes=False)
def is_number(n):
    """Route to display 'n is a number' only if n is a number"""
    return f"{n} is a number"


@app.route("/number_template/<int:n>", strict_slashes=False)
def display_html_page0(n):
    """Route to display an html page only if n is a number"""
    return render_template('5-number.html', n=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
