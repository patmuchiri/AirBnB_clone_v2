#!/usr/bin/python3

""" List of states """
from models import storage
from models.state import State
from flask import Flask, render_template

app = Flask(__name__)


@app.teardown_appcontext
def remove_sqlalchemy_session(self):
    """  remove the current SQLAlchemy Session """
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """list of all State objects present in DBStorage"""

    return render_template('7-states_list.html',
                           states=storage.all(State))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
