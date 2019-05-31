import traceback
from flask import render_template, request, redirect, url_for
import logging.config
# from app.models import Channel
from flask import Flask
from src.add_Channel import Channel
from flask_sqlalchemy import SQLAlchemy

import random

# Initialize the Flask application
app = Flask(__name__)

# Configure flask app from flask_config.py
app.config.from_pyfile('../config/flask_config.py')

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger("penny-lane")
logger.debug('Test log')

# Initialize the database
db = SQLAlchemy(app)


# @app.route('/')
# def index():
#     """Main view that lists songs in the database.

#     Create view into index page that uses data queried from Track database and
#     inserts it into the msiapp/templates/index.html template.

#     Returns: rendered html template

#     """

#     try:
#         tracks = db.session.query(Tracks).limit(app.config["MAX_ROWS_SHOW"]).all()
#         logger.debug("Index page accessed")
#         return render_template('index.html', tracks=tracks)
#     except:
#         traceback.print_exc()
#         logger.warning("Not able to display tracks, error page returned")
#         return render_template('error.html')


@app.route('/add', methods=['POST'])
def add_entry():
    """View that process a POST with new channel input

    :return: redirect to index page
    """

    try:
        channelID = str(random.randint(1, 999999999))
        channel1 = Channel(channelID = , channelDays = request.form['channelDays'], viewCount = request.form['viewCount'], likes=request.form['likes'], dislikes=request.form['dislikes'], videoCount=request.form['videoCount'], commentCount=request.form['commentCount'])
        db.session.add(channel1)
        db.session.commit()
        logger.info("Channel with %s days, %s likes, %s dislikes, %s videos, %s comments, %s views, added to database",
        request.form['channelDays'], request.form['likes'], request.form['dislikes'], request.form['videoCount'], request.form['commentCount'], request.form['viewCount'])
        return redirect(url_for('index'))
    except:
        logger.warning("Not able to display tracks, error page returned")
        return render_template('error.html')


