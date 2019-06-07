import os
import sys
import logging
import logging.config
import sqlalchemy as sql

from sqlalchemy import create_engine, Column, Integer, String, Text, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData

#import config
import yaml
from helpers.helpers import create_connection, get_session
import argparse

logging.basicConfig(level=logging.INFO, format="%(name)-12s %(levelname)-8s %(message)s")
logger = logging.getLogger()

Base = declarative_base()


class YouTube(Base):

    """ Defines the data model for the table `YouTube`. """

    __tablename__ = 'YouTube'

    VideoCommentCount = Column(String(100), unique=False, nullable=False)
    channelCommentCount = Column(String(100), unique=False, nullable=False)
    channelId = Column(String(100), primary_key=True, unique=True)
    channelViewCount = Column(String(100), unique=False, nullable=False)
    channelelapsedtime = Column(String(100), unique=False, nullable=False)
    comments_subscriber = Column(String(100), unique=False, nullable=False)
    comments_views = Column(String(100), unique=False, nullable=False)
    dislikes_subscriber = Column(String(100), unique=False, nullable=False)
    dislikes_views = Column(String(100), unique=False, nullable=False)
    elapsedtime = Column(String(100), unique=False, nullable=False)
    likes_dislikes = Column(String(100), unique=False, nullable=False)
    likes_subscriber = Column(String(100), unique=False, nullable=False)
    likes_views = Column(String(100), unique=False, nullable=False)
    subscriberCount = Column(String(100), unique=False, nullable=False)
    totalviews_channelelapsedtime = Column(String(100), unique=False, nullable=False)
    totvideos_videocount = Column(String(100), unique=False, nullable=False)
    totviews_totsubs = Column(String(100), unique=False, nullable=False)
    videoCategoryId = Column(String(100), unique=False, nullable=False)
    videoCount = Column(String(100), unique=False, nullable=False)
    videoDislikeCount = Column(String(100), unique=False, nullable=False)
    videoId = Column(Text, unique=False, nullable=False)
    videoLikeCount = Column(Text, unique=False, nullable=False)
    videoPublished = Column(Text, unique=False, nullable=False)
    videoViewCount = Column(String(100), unique=False, nullable=False)
    views_elapsedtime = Column(String(100), unique=False, nullable=False)
    views_subscribers = Column(String(100), unique=False, nullable=False)

    def __repr__(self):
        YouTube_repr = "<YouTube(VideoCommentCount='%s', channelCommentCount='%s', channelId='%s', channelViewCount='%s', channelelapsedtime='%s', comments_subscriber='%s', comments_views='%s', dislikes_subscriber='%s', dislikes_views='%s', elapsedtime='%s', likes_dislikes='%s',likes_subscriber='%s', likes_views='%s', subscriberCount='%s', totalviews_channelelapsedtime='%s', totvideos_videocount='%s', totviews_totsubs='%s', videoCategoryId='%s', videoCount='%s', videoDislikeCount='%s', videoId, self.videoLikeCount='%s', videoPublished='%s', videoViewCount='%s', views_elapsedtime='%s', views_subscribers='%s')>"
        return YouTube_repr % (self.VideoCommentCount, self.channelCommentCount, self.channelId, self.channelViewCount, self.channelelapsedtime,
            self.comments_subscriber, self.comments_views, self.dislikes_subscriber, self.dislikes_views, self.elapsedtime, self.likes_dislikes,
            self.likes_subscriber, self.likes_views, self.subscriberCount, self.totalviews_channelelapsedtime, self.totvideos_videocount, self.totviews_totsubs,
            self.videoCategoryId, self.videoCount, self.videoDislikeCount, self.videoId, self.videoLikeCount, self.videoPublished, self.videoViewCount, 
            self.views_elapsedtime. self.views_subscribers)

class Channel(Base):

    """ Defines the data model for the table `channel`. """

    __tablename__ = 'channel'

    channelID = Column(String(100), primary_key=True, unique=False, nullable=False)
    channelDays = Column(String(100), unique=False, nullable=False)
    viewCount = Column(String(100), unique=False, nullable=False)
    likes = Column(String(100), unique=False, nullable=False)
    dislikes = Column(String(100), unique=False, nullable=False)
    videoCount = Column(String(100), unique=False, nullable=False)
    commentCount = Column(String(100), unique=False, nullable=False)
    catID = Column(String(100), unique=False, nullable=False)
    pred1 = Column(String(100), unique=False, nullable=False)
    pred2 = Column(String(100), unique=False, nullable=False)
    pred3 = Column(String(100), unique=False, nullable=False)
    pred4 = Column(String(100), unique=False, nullable=False)

    def __repr__(self):
        Channel_repr = "<Channel(channelID='%s', channelDays='%s', viewCount='%s', likes='%s', dislikes='%s', videoCount='%s', commentCount='%s', catID='%s')>"
        return Channel_repr % (self.channelID, self.channelDays, self.viewCount, self.likes, self.dislikes, self.videoCount, self.commentCount, self.catID)


def _truncate_Channel(session):
    """Deletes Channel table if rerunning and run into unique key error."""

    session.execute('''DELETE FROM channel''')

def _truncate_YouTube(session):
    """Deletes YouTube table if rerunning and run into unique key error."""

    session.execute('''DELETE FROM YouTube''')


def create_db(args):
    """Creates a database with the data models inherited from `Base` (YouTube and Channel).

    Args:
        engine (:py:class:`sqlalchemy.engine.Engine`, default None): SQLAlchemy connection engine.
            If None, `engine_string` must be provided.
        engine_string (`str`, default None): String defining SQLAlchemy connection URI in the form of
            `dialect+driver://username:password@host:port/database`. If None, `engine` must be provided.

    Returns:
        None
    """
    
    #create engine
    engine_string = get_engineString(args.use_sqlite)
    print(engine_string)
    engine = sql.create_engine(engine_string)
    Base.metadata.create_all(engine)

    ## End of function
    logging.info('------------- Database Created ------------')

def get_engineString(use_sqlite):
    """Get engine string from setting and environment

    Args: 
        None

    Returns:
        Engine String
    """

    ## If using local database
    if use_sqlite is True:
        engine_string = "sqlite:///data/channel.db"

    ## If using RDS
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
        conn_type = "mysql+pymysql"
        user = os.environ.get("MYSQL_USER")
        password = os.environ.get("MYSQL_PASSWORD")
        host = os.environ.get("MYSQL_HOST")
        port = os.environ.get("MYSQL_PORT")
        DATABASE_NAME = 'msia423ywzhang'
        engine_string = "{}://{}:{}@{}:{}/{}".\
        format(conn_type, user, password, host, port, DATABASE_NAME)


    ## End of function
    logging.info('------------- Engine String Retrieved ------------')

    return(engine_string)

def add_channel(args):
    """Seeds an existing database with additional channels.

    Args:
        args: Argparse args - should include args.channelID,    args.channelDays, args.viewCount, args.likes, args.dislikes, args.videoCount, args.commentCount, args.catID

    Returns:None

    """

    engine_string = get_engineString(args.use_sqlite)
    session = get_session(engine_string=engine_string)

    channel = Channel(channelID=args.channelID, channelDays = args.channelDays, viewCount = args.viewCount, likes=args.likes, dislikes=args.dislikes, videoCount=args.videoCount, commentCount=args.commentCount, catID=args.catID, pred1=args.pred1, pred2=args.pred2, pred3=args.pred3, pred4=args.pred4)
    session.add(channel)
    session.commit()
    logger.info("Channel with %s days, %s likes, %s dislikes, %s videos, %s comments, %s views, %s catID added to database",
        args.channelDays, args.likes, args.dislikes, args.videoCount, args.commentCount, args.viewCount, args.catID)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create defined tables in database and add new entries")
    subparsers = parser.add_subparsers()

    # Sub-parser for creating a database
    sb_create = subparsers.add_parser("create", description="Create database")
    sb_create.add_argument("--use_sqlite", default=False, help="Use local or RDS database")
    sb_create.add_argument("--channelID", default="103382913", help="Channel ID")
    sb_create.add_argument("--channelDays", default="103", help="Days the channel has been created")
    sb_create.add_argument("--viewCount", default="48729", help="Total views of the channel")
    sb_create.add_argument("--likes", default="8728", help="Total likes of the channel")
    sb_create.add_argument("--dislikes", default="2637", help="Total dislikes of the channel")
    sb_create.add_argument("--commentCount", default="3728", help="Total comments of the channel")
    sb_create.add_argument("--videoCount", default="347", help="Total videos of the channel")
    sb_create.add_argument("--catID", default="34", help="Category ID")
    sb_create.add_argument("--pred1", default="10000", help="Prediction 1")
    sb_create.add_argument("--pred2", default="20000", help="Prediction 2")
    sb_create.add_argument("--pred3", default="30000", help="Prediction 3")
    sb_create.add_argument("--pred4", default="40000", help="prediction 4")
    sb_create.add_argument("--truncate", "-t", default=False, action="store_true",
                        help="If given, delete current records from YouTube table before create_all "
                             "so that table can be recreated without unique id issues ")
    sb_create.set_defaults(func=create_db)

    # Sub-parser for ingesting new data
    sb_ingest = subparsers.add_parser("ingest", description="Add data to database")
    sb_ingest.add_argument("--use_sqlite", default=False, help="Use local or RDS database")
    sb_ingest.add_argument("--channelID", default="74829103", help="Channel ID")
    sb_ingest.add_argument("--channelDays", default="736", help="Days the channel has been created")
    sb_ingest.add_argument("--viewCount", default="528920", help="Total views of the channel")
    sb_ingest.add_argument("--likes", default="96372", help="Total likes of the channel")
    sb_ingest.add_argument("--dislikes", default="19438", help="Total dislikes of the channel")
    sb_ingest.add_argument("--commentCount", default="28475", help="Total comments of the channel")
    sb_ingest.add_argument("--videoCount", default="769", help="Total videos of the channel")
    sb_ingest.add_argument("--catID", default="34", help="Category ID")
    sb_ingest.add_argument("--pred1", default="10000", help="Prediction 1")
    sb_ingest.add_argument("--pred2", default="20000", help="Prediction 2")
    sb_ingest.add_argument("--pred3", default="30000", help="Prediction 3")
    sb_ingest.add_argument("--pred4", default="40000", help="prediction 4")
    sb_ingest.add_argument("--truncate", "-t", default=False, action="store_true",
                        help="If given, delete current records from YouTube table before create_all "
                             "so that table can be recreated without unique id issues ")
    sb_ingest.set_defaults(func=add_channel)

    args = parser.parse_args()
    args.func(args)

    # If "truncate" is given as an argument (i.e. python models.py --truncate), then empty the Channel table)
    if args.truncate:
        session = get_session(engine_string=get_engineString(args.use_sqlite))
        try:
            logger.info("Attempting to truncate Channel table.")
            _truncate_Channel(session)
            session.commit()
            logger.info("Channel truncated.")
        except Exception as e:
            logger.error("Error occurred while attempting to truncate Channel table.")
            logger.error(e)
        finally:
            session.close()

    # engine_string = get_engineString()

    # ## Create database
    # create_db(engine_string)

    ## Testing -- Add Data
    # create a db session
    # Session = sessionmaker(bind=engine)
    # session = Session()

    # # add a channel and print
    # channel1 = Channel(channelDays='324', viewCount='273', likes='473', dislikes = '238', videoCount='2732', commentCount='372')
    # session.add(channel1)
    # logger.info("------------- New Channel Added ------------- ")
    # tbl = session.execute("SELECT * FROM Channel")
    # print(tbl)

    # session.commit()
    # logger.info("------------- Data Table Printed ------------- ")






