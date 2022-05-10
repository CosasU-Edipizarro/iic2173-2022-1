from db.models import ENV, Session
from db.populate import users

def db_populate():
    if ENV['DB_DROP'] and ENV['DB_POPULATE']:
        db = Session()
        users.create_users(db)
        db.commit()
        db.close()

