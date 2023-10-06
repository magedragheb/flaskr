import sqlite3
import click
from flask import current_app, g

def get_db():
    '''returns a database connection'''
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    '''initialize the database'''
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    '''calls init_db() and prints a message'''
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    '''registers the database commands with app'''
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)