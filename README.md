# podbeetle
A simple website to search for keywords in your favourite podcasts. - http://www.podbeetle.com

## Install
The web app is using the [Python Flask](http://flask.pocoo.org/) framework for the website and the [Deepgram API](https://www.deepgram.com) for the audio file transcription.

### Requirements
Install all the requirements with:
```bash
pip install -r requirements.txt
```


You will need to have a Deepgram API account in order to be able to upload/index/transcribe audio files to their API.

Set the API key as an enviroment variable:
```bash
export DEEPGRAM_API_KEY=<api-key>
```

### Database
This implementation is using a PostgreSQL database. You can install it from the [website](https://www.postgresql.org/download/) or you can use the official Docker [image](https://hub.docker.com/_/postgres/) instead.

Alternatively, you can edit the `database.py` file and update the [database engine](https://github.com/agouil/podbeetle/blob/master/database.py#L7) to the one you'd like to use.

After installing and starting the database, set the following enviroment variables:
```bash
export DB_USER=<database-user>
export DB_PASS=<database-password>
export DB_HOST=<database-host>
export DB_PORT=<database-port>
export DB_NAME=<database-name>
```

Run the following script to initialize the database based on the models defined in `models.py` file:
```bash
python scripts.py init_db
```

Once the database is initialized then you can populate it with some data by running:
```bash
python scripts.py populate_db
```

### Uploading files to Deepgram
After populating the database, run the following script to upload/index/trasncribe the audio files with the Deepgram API.
```bash
python scripts.py deepgram_upload
```

After this step is complete you'll be able to run the app and search for keywords in these podcasts.

### Run the app
To run the app, simply:
1. Set the Flask enviroment variable: `export FLASK_APP=app.py`
2. Run the Flask app with: `flask run`

## Contributing
Pull requests are welcome! :muscle:

## Issues
To submit any issues, raise an issue through the [Issues Page](https://github.com/agouil/podbeetle/issues)

## License
[MIT](LICENSE)

