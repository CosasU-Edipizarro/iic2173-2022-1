from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

def db_init(DB_URI, DEBUG=False):

    # Create engine
    # engine = create_engine(DB_URI, pool_size=200, pool_recycle=280, max_overflow=-1)
    engine = create_engine(DB_URI, echo=DEBUG)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

    db = {
        'engine': engine,
        'Session': Session,
        'Base': Base
    }

    return db
