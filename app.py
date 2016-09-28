import json

from config import DEEPGRAM_API_KEY
from database import db_session
from deepgram import Deepgram
from math import floor
from models import Podcast
from flask import Flask, render_template, request, Response

app = Flask(__name__)


@app.route('/')
def index():
    podcasts = Podcast.query.order_by(Podcast.remote_id).all()
    return render_template("index.html", **{
        "podcasts": podcasts
    })


@app.route('/search')
def search():
    query = request.args.get("query", "")
    dg_client = Deepgram(DEEPGRAM_API_KEY)

    # make search request to API
    search_result = dg_client.parallel_search(query, **{
        "tag": "podcast",
        "snippet": True,
        "group_Nmax": 100,
        "object_Nmax": 1,
        "object_Pmin": 0.8
    })

    # construct response to send back
    result = []
    for item in search_result["object_result"]:
        if not item["N"]:
            continue
        # grab item from local database
        local_item = Podcast.query.filter(
            Podcast.remote_id == item["contentID"]).first()
        result_item = {
            "name": local_item.name,
            "author": local_item.author,
            "title": local_item.title,
            "image": local_item.image,
            "url": local_item.url
        }
        # format start time (add 2 seconds leading time)
        start_time = floor(item["startTime"][0])
        if start_time - 2 > 0:
            result_item["start_time"] = start_time - 2
        else:
            result_item["start_time"] = start_time

        # append to final result
        result.append(result_item)

    return Response(json.dumps({"result": result}), mimetype='text/json')


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
