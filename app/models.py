import logging
from app import db

logger = logging.getLogger(__name__)

db.Model.metadata.reflect(db.engine)


class Channel(db.Model):
    """Create a data model for the database to be set up for new channels

    """
    try:
        __table__ = db.Model.metadata.tables['channels'] 
    except:
        logger.warning("'channels' table not found")

    def __repr__(self):
        return Channel_repr % (self.channelID, self.channelDays, self.viewCount, self.likes, self.dislikes, self.videoCount, self.commentCount)
