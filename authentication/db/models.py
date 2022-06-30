import datetime
from email.policy import default
from operator import index

from sqlalchemy import Column, Integer, Float, Boolean, DateTime, Date, ForeignKey, Text
from sqlalchemy.orm import relationship

from db.engine import db_init
from db.db_utils import load_env


# Import .env
ENV = load_env()

# Initialize Database
db = db_init(ENV['DATABASE_URI'], ENV['DEBUG'])

engine = db['engine']
Session = db['Session']
Base = db['Base']

# Dependency
def get_db():
    print("METHOD: get_db()")
    db = Session()
    print("get_db: Session created")
    try:
        print("get_db: Yield session")
        yield db
    finally:
        print("get_db: Closing session")
        db.close()


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True, index=True)
    name = Column(Text(), nullable=False)
    username = Column(Text(), unique=True, nullable=False)
    email = Column(Text(), unique=True, nullable=False)
    phone = Column(Text(), unique=True)
    hashed_password = Column(Text(), nullable=False)
    verified = Column(Boolean(), default=False)
    uuid = Column(Text(), unique=True, nullable=False)

    token = relationship("Token", back_populates="user", uselist=False)


class Token(Base):

    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True, index=True)
    access_token = Column(Text(), nullable=False, index=True)
    token_type = Column(Text(), nullable=False, index=True)

    user_id = Column(Integer(), ForeignKey('users.id'), index=True)
    user = relationship("User", back_populates="token")


class VerificationEmail(Base):

    __tablename__ = 'verification_emails'

    id = Column(Integer, primary_key=True, index=True)
    access_token = Column(Text(), nullable=False, index=True)

    user_id = Column(Integer(), ForeignKey('users.id'), index=True)
    user = relationship("User")