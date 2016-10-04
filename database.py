from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('postgresql+psycopg2://%s:%s@%s:%s/%s' % (
    DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME))
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.create_all(bind=engine)
