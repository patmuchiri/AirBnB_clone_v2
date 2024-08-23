#!/usr/bin/python3

""" Hello Flask! simple flask app """

from flask import Flask

app = Flask(__name__)


@app.route('/airbnb-onepage/', strict_slashes=False)
def hello():
    """ route that displays some text """
    return "Hello HBNB!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
