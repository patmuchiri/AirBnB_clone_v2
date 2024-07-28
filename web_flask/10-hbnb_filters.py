#!/usr/bin/python3

""" HBNB filters site """
from models import storage
from models.state import State
from models.amenity import Amenity
from flask import Flask, render_template

app = Flask(__name__)


@app.teardown_appcontext
def remove_sqlalchemy_session(self):
    """  remove the current SQLAlchemy Session """
    storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """list of all State objects and Amenities present in DBStorage"""

    return render_template('10-hbnb_filters.html',
                           states=storage.all(State),
                           amenities=storage.all(Amenity))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
