from database import db_session
from models import Podcast
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    podcasts = Podcast.query.all()
    return render_template("index.html", **{
        "podcasts": podcasts
    })


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
