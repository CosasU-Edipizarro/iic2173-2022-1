import os

def load_env():
    ENV = dict()
    ENV['DEBUG'] = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 't')
    ENV['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'foo')
    ENV['JWT_SECRET'] = os.environ.get('JWT_SECRET', 'secret')

    ENV['DBUSER'] = os.environ.get('POSTGRES_USER', 'secret')
    ENV['DBPASSWD'] = os.environ.get('POSTGRES_PASSWORD', 'secret')
    ENV['DBHOST'] = os.environ.get('POSTGRES_HOST', 'secret')
    ENV['DBDATABASE'] = os.environ.get('POSTGRES_DB', 'secret')
    ENV['DATABASE_URI'] = f"postgresql://{ENV['DBUSER']}:{ENV['DBPASSWD']}@{ENV['DBHOST']}/{ENV['DBDATABASE']}"

    ENV['DB_CREATE'] = os.environ.get('DB_CREATE', 'False').lower() in ('true', '1', 't')
    ENV['DB_DROP'] = os.environ.get('DB_DROP', 'False').lower() in ('true', '1', 't')
    print(f"ENV DB_CREATE: {ENV['DB_CREATE'] == True}")
    print(f"ENV DB_DROP: {ENV['DB_DROP'] == True}")

    ENV['EMAIL_HOST'] = os.environ.get('EMAIL_HOST', 'localhost')
    ENV['EMAIL_PORT'] = int(os.environ.get('EMAIL_PORT', 25))

    return ENV