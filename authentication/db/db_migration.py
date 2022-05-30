from db.models import ENV, Base, engine
# from db.models import Base, engine, User, Location, JWT

def create_tables():
    print("¡¡ create_tables() !!")
    Base.metadata.create_all(bind=engine)

def drop_tables():
    print("¡¡ drop_tables() !!")
    Base.metadata.drop_all(bind=engine)

def db_migration():
    if ENV['DB_DROP']:
        drop_tables()
    if ENV['DB_CREATE']:
        create_tables()
