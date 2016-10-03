import argparse
import csv
import sys

from config import DEEPGRAM_API_KEY
from database import db_session, init_db
from deepgram import Deepgram
from models import Podcast
from time import sleep


def populate_db():
    """
    Populates the database with the contents of the 'podcast_data.csv' file
    """

    with open("./db/podcast_data_dump.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            p = Podcast(row["name"].decode('utf8'), row["author"],
                        row["title"].decode('utf8'), row["image"],
                        row["url"])

            # if data has remote_id property then add to db
            if "remote_id" in row:
                p.remote_id = row["remote_id"]
            db_session.add(p)
        # commit changes to db
        db_session.commit()
        # close db session
        db_session.remove()


def dump_db():
    """
    Dumps database data into a CSV file.
    """

    podcasts = Podcast.query.all()

    headers = ["name", "author", "title", "image", "url", "remote_id"]
    with open("./db/podcast_data_dump.csv", "w") as csvfile:
        writer = csv.DictWriter(
            csvfile, fieldnames=headers, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for podcast in podcasts:
            writer.writerow({
                "name": podcast.name,
                "author": podcast.author,
                "title": podcast.title,
                "image": podcast.image,
                "url": podcast.url,
                "remote_id": podcast.remote_id
            })


def deepgram_upload():
    """
    Uploads any new podcasts to Deepgram API
    """

    dg = Deepgram(DEEPGRAM_API_KEY)

    podcasts_to_upload = Podcast.query.filter(
        Podcast.remote_id == "").limit(15).all()

    # podcasts_to_upload = Podcast.query.filter(Podcast.remote_id == "").all()

    for podcast in podcasts_to_upload:
        upload_response = dg.upload(podcast.url, ["podcast"])

        # check status
        while True:
            status_response = dg.check_status(upload_response["contentID"])
            if status_response["status"] == "fetch":
                # sleep 1 sec
                sleep(1)
                continue
            elif status_response["status"] in [
                    "transcode", "chunk", "awaiting_gen_lattice"]:
                # sleep 5 secs
                # TODO: periodically check the server until is done
                break
            elif status_response["status"] == "done":
                break

        # update podcast with new remote_id
        podcast.remote_id = upload_response["contentID"]
        db_session.add(podcast)
    # commit changes to db
    db_session.commit()
    # close db session
    db_session.remove()


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('UTF8')

    parser = argparse.ArgumentParser(prog="python scripts.py")
    parser.add_argument("script", help="the script to run")
    args = parser.parse_args()

    if args.script == "populate_db":
        populate_db()
    elif args.script == "deepgram_upload":
        deepgram_upload()
    elif args.script == "init_db":
        init_db()
    elif args.script == "dump_db":
        dump_db()
