import flask
import psycopg2
import psycopg2.extras
from . import config

def get_connection():
    if not hasattr(flask.g, 'dbconn'):
        flask.g.dbconn = psycopg2.connect(
            database=config.ProductionConfig.DB_NAME, host=config.ProductionConfig.DB_HOST,
            user=config.ProductionConfig.DB_USER, password=config.ProductionConfig.DB_PASS)
    return flask.g.dbconn

def get_cursor():
    return get_connection().cursor(
        cursor_factory=psycopg2.extras.DictCursor)

def query_one(sql, **params):
    with get_cursor() as cur:
        cur.execute(sql, params)
        return dict(cur.fetchone())

def query_all(sql, **params):
    with get_cursor() as cur:
        cur.execute(sql, params)
        value = []
        for row in cur.fetchall():
            value.append(row)
        index = list(range(0, len(value)))
        return dict(zip(index, value))

def update_base(sql, **params):
    with get_cursor() as cur:
        cur.execute(sql, params)

def _rollback_db(exception, **extra):
    if hasattr(flask.g, 'dbconn'):
        conn = flask.g.dbconn
        conn.rollback()
        #conn.close()
        delattr(flask.g, 'dbconn')

def _commit_db(exception, **extra):
    if hasattr(flask.g, 'dbconn'):
        conn = flask.g.dbconn
        conn.commit()
        #conn.close()

