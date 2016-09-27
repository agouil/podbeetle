from database import Base
from sqlalchemy import Column, Integer, String


class Podcast(Base):
    __tablename__ = 'podcast'
    id = Column(Integer, primary_key=True)
    remote_id = Column(String(256), unique=True)
    name = Column(String(512))
    author = Column(String(128))
    image = Column(String(512))
    url = Column(String(512))

    def __init__(self, name, author, image, url, remote_id=None):
        self.name = name
        self.author = author
        self.image = image
        self.url = url
        self.remote_id = remote_id

    def __repr__(self):
        return '<Podcast %s - %s>' % (self.author, self.name)
