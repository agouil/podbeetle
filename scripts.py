import argparse
import csv
import sys

from database import db_session, init_db
from models import Podcast


def populate_db():
    """
    Populates the database with the contents of the 'podcast_data.csv' file
    """

    with open("./db/podcast_data.csv", "r") as csvfile:
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


def deepgram_upload():
    """
    Uploads any new podcasts to Deepgram API
    """

    pass


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
