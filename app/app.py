import traceback
from flask import render_template, request, redirect, url_for
import logging.config
from flask import Flask
from src.addChannel import Channel
from flask_sqlalchemy import SQLAlchemy

# For Prediction
import random
import pandas as pd
import numpy as np

# Initialize the Flask application
app = Flask(__name__)

# Configure flask app from flask_config.py
app.config.from_object('config')

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
# logging.config.fileConfig(app.config["LOGGING_CONFIG"])
# logger = logging.getLogger("youtube-yiwei")

logging.basicConfig(level=logging.INFO, format="%(name)-12s %(levelname)-8s %(message)s")
logger = logging.getLogger()
logger.debug('Test log')

# Initialize the database
db = SQLAlchemy(app)

# Import prediction file here
from predictNew import NewPredict
newpredict = NewPredict()


@app.route('/')
def index():
    """Main view that asks for user input

    Create view into index page that uses data queried from Channel database and
    inserts it into the templates/index.html template.

    Returns: rendered html template

    """

    return render_template('index.html', result1='', result2='', result3='', result4='', img_path='static/prediction1.png')

# @app.route('/add', methods=['POST'])
# def add_entry():
#     """View that process a POST with new channel input

#     :return: redirect to index page
#     """

#     try:
#         logger.info("---- Adding started ----")
#         channel2 = Channel(channelDays = request.form['channelDays'], viewCount = viewCount, likes=request.form['likes'], dislikes=request.form['dislikes'], videoCount=request.form['videoCount'], commentCount=request.form['commentCount'])
#         logger.info("second entry entered")

#         db.session.add(channel2)
#         logger.info("second entry added")

#         db.session.commit()
#         logger.info("committed")

#         logger.info("Channel with %s days, %s likes, %s dislikes, %s videos, %s comments, %s views, added to database",
#         request.form['channelDays'], request.form['likes'], request.form['dislikes'], request.form['videoCount'], request.form['commentCount'], viewCount)
#         return redirect(url_for('index'))
#     except:
#         traceback.print_exc()
#         logger.warning("Not able to display tracks, error page returned")
#         return render_template('error.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Predict new input data

    :return: redirect to index page
    """

    try:
        ## Predict new data
        logger.info("---- Adding Data Started ----")
        days = float(request.form['channelDays'])
        likes = float(request.form['likes'])
        dislikes = float(request.form['dislikes'])
        videoCount = float(request.form['videoCount'])
        commentCount = float(request.form['commentCount'])
        viewCount = float(request.form['viewCount'])
        catID = float(request.form['catID'])
        channelID = str(random.randint(1,999999999))

        #new features goes here, all variables ready for predict 
        view_days = viewCount / days
        likes_views = likes / viewCount
        totvideo_videoCount = 1
        videoLike = likes
        comment_views = commentCount / viewCount
        dislikes_views = dislikes / viewCount
        videodislike = dislikes
        likes_dislikes = likes / dislikes

        logger.info("---- Feature Calculation Done ----")

        #add to df and reshape
        newdata = [viewCount, view_days, likes_views, totvideo_videoCount, videoCount, videoLike, commentCount, comment_views, dislikes_views, videodislike, catID, likes_dislikes, days]
        newdf = pd.DataFrame(np.array(newdata).reshape(1,13))

        logger.info("---- Predicting Started ----")
        result1, result2, result3, result4, img_path = newpredict.run(newdf)
        logger.info("---- Prediction Done ----")

        # Add result to database
        logger.info("---- Adding data to db started ----")
        channel = Channel(channelID = channelID, channelDays = request.form['channelDays'], viewCount = request.form['viewCount'], 
            likes=request.form['likes'], dislikes=request.form['dislikes'], videoCount=request.form['videoCount'], commentCount=request.form['commentCount'], 
            catID=request.form['catID'], pred1=result1, pred2=result2, pred3=result3, pred4=result4)
        logger.info("---- Entry entered ---- ")

        db.session.add(channel)
        logger.info("---- Entry added ----")

        db.session.commit()
        logger.info("---- Committed ----")

        logger.info("Channel with %s days, %s likes, %s dislikes, %s videos, %s comments, %s views, added to database",
        request.form['channelDays'], request.form['likes'], request.form['dislikes'], request.form['videoCount'], request.form['commentCount'], viewCount)

        # show on page
        return render_template('index.html', result1=result1, result2=result2, result3=result3, result4=result4, img_path=img_path)

    except:
        traceback.print_exc()
        logger.warning("Not able to predict and insert new data to the database, try entering valid input")
        return render_template('error.html')



