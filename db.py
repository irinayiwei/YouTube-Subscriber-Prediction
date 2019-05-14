import os
import sys
import logging
import logging.config

from sqlalchemy import create_engine, Column, Integer, String, Text, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#import config
#from helpers import create_connection, get_session
import argparse

#logging.config.fileConfig(config.LOGGING_CONFIG)
#logger = logging.getLogger('sportco-models')

Base = declarative_base()


class YouTube(Base):
    """ Defines the data model for the table `YouTube`. """

    __tablename__ = 'YouTube'

    VideoCommentCount = Column(String(100), unique=False, nullable=False)
    channelCommentCount = Column(String(100), unique=False, nullable=False)
    channelId = Column(String(100), primary_key=True, unique=True, nullable=False)
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

class YouTubeInput(Base):
    """ Defines the data model for the table `YouTubeInput`. """

    __tablename__ = 'YouTubeInput'

    channelId = Column(String(100), primary_key=True, unique=True, nullable=False)
    channelDays = Column(String(100), unique=False, nullable=False)
    channelViewCount = Column(String(100), unique=False, nullable=False)
    totalviews_channelelapsedtime = Column(String(100), unique=False, nullable=False)
    likes_views = Column(String(100), unique=False, nullable=False)
    totvideos_videocount = Column(String(100), unique=False, nullable=False)
    videoCount = Column(String(100), unique=False, nullable=False)
    videoLikeCount = Column(Text, unique=False, nullable=False)
    channelCommentCount = Column(String(100), unique=False, nullable=False)
    comments_views = Column(String(100), unique=False, nullable=False)
    dislikes_views = Column(String(100), unique=False, nullable=False)
    videoDislikeCount = Column(String(100), unique=False, nullable=False)
    videoCategoryId = Column(String(100), unique=False, nullable=False)
    likes_dislikes = Column(String(100), unique=False, nullable=False)
    pred = Column(String(100), unique=False, nullable=False)


    def __repr__(self):
        YouTubeInput_repr = "<YouTubeInput(channelID='%s', channelDays='%s', channelViewCount='%s', totalviews/channelelapsedtime='%s', likes/views='%s', totvideos/videocount='%s', videoCount='%s', videoLikeCount='%s', channelCommentCount='%s', comments/views='%s', dislikes/views='%s', videoDislikeCount='%s', videoCategoryId='%s', likes/dislikes='%s', pred='%s')>"
        return YouTubeInput_repr % (self.channelID, self.channelDays, self.channelViewCount, self.totalviews_channelelapsedtime, self.likes_views, self.totvideos_videocount, 
            self.videoCount, self.videoLikeCount, self.channelCommentCount, self.comments_views, self.dislikes_views,
            self.videoDislikeCount, self.videoCategoryId, self.likes_dislikes, self.pred)


def _truncate_YouTubeInput(session):
    """Deletes YouTubeInput table if rerunning and run into unique key error."""

    session.execute('''DELETE FROM YouTubeInput''')

def _truncate_YouTube(session):
    """Deletes YouTube table if rerunning and run into unique key error."""

    session.execute('''DELETE FROM YouTube''')


def create_db(engine=None, engine_string=None):
    """Creates a database with the data models inherited from `Base` (YouTube and YouTubeInput).

    Args:
        engine (:py:class:`sqlalchemy.engine.Engine`, default None): SQLAlchemy connection engine.
            If None, `engine_string` must be provided.
        engine_string (`str`, default None): String defining SQLAlchemy connection URI in the form of
            `dialect+driver://username:password@host:port/database`. If None, `engine` must be provided.

    Returns:
        None
    """
    if engine is None and engine_string is None:
        return ValueError("`engine` or `engine_string` must be provided")
    elif engine is None:
        engine = create_connection(engine_string=engine_string)

    Base.metadata.create_all(engine)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create defined tables in database")
    parser.add_argument("--truncate", "-t", default=False, action="store_true",
                        help="If given, delete current records from YouTube table before create_all "
                             "so that table can be recreated without unique id issues ")
    args = parser.parse_args()

    # If "truncate" is given as an argument (i.e. python models.py --truncate), then empty the tweet_score table)
    if args.truncate:
        #session = get_session(engine_string=config.SQLALCHEMY_DATABASE_URI)
        try:
            logger.info("Attempting to truncate YouTubeInput table.")
            _truncate_YouTubeInput(session)
            session.commit()
            logger.info("YouTubeInput truncated.")
        except Exception as e:
            logger.error("Error occurred while attempting to truncate YouTubeInput table.")
            logger.error(e)
        finally:
            session.close()

    engine_string = "{conn_type}://{user}:{password}@{host}:{port}/{database}"
    engine = sql.create_engine(engine_string)

    create_db(engine)

    # Add Data
    # set up looging config
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__file__)
    # create a db session
    Session = sessionmaker(bind=engine)
    session = Session()
    # add a record/track
    track1 = Track(channelID='123jieife2', channelDays='324', channelViewCount='273', totalviews_channelelapsedtime='283.3', likes_views='473.3554', totvideos_videocount='32', videoCount='2732', videoLikeCount='232', channelCommentCount='327382', comments_views='23296', dislikes_views='-34.2', videoDislikeCount='86', videoCategoryId='788', likes_dislikes='096', pred='983265478')
    session.add(track1)
    session.commit()
    logger.info("Database created with new input added")




