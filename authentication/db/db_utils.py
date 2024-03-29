import os

def load_env():
    ENV = dict()
    ENV['DEBUG'] = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 't')
    ENV['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'foo')
    ENV['ALGORITHM'] = os.environ.get('ALGORITHM', 'bar')
    ENV['ACCESS_TOKEN_EXPIRE_MINUTES'] = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES', '9000'))
    ENV['JWT_SECRET'] = os.environ.get('JWT_SECRET', 'secret')

    ENV['DBUSER'] = os.environ.get('POSTGRES_USER', 'secret')
    ENV['DBPASSWD'] = os.environ.get('POSTGRES_PASSWORD', 'secret')
    ENV['DBHOST'] = os.environ.get('POSTGRES_HOST', 'secret')
    ENV['DBDATABASE'] = os.environ.get('POSTGRES_DB', 'secret_db')
    ENV['DATABASE_URI'] = f"postgresql://{ENV['DBUSER']}:{ENV['DBPASSWD']}@{ENV['DBHOST']}/{ENV['DBDATABASE']}"

    ENV['DB_CREATE'] = os.environ.get('DB_CREATE', 'False').lower() in ('true', '1', 't')
    ENV['DB_DROP'] = os.environ.get('DB_DROP', 'False').lower() in ('true', '1', 't')
    ENV['DB_POPULATE'] = os.environ.get('DB_POPULATE', 'False').lower() in ('true', '1', 't')
    print(f"ENV DB_CREATE: {ENV['DB_CREATE'] == True}")
    print(f"ENV DB_DROP: {ENV['DB_DROP'] == True}")
    print(f"ENV DB_POPULATE: {ENV['DB_POPULATE'] == True}")

    ENV['EMAIL_HOST'] = os.environ.get('EMAIL_HOST', 'localhost')
    ENV['EMAIL_PORT'] = int(os.environ.get('EMAIL_PORT', 25))

    ENV['SENDGRID_API_KEY'] = os.environ.get('SENDGRID_API_KEY', 'secret_sendgrid')
    
    ENV['URL_API'] = os.environ.get('URL_API', 'localhost:8000')
    ENV['URL_AUTH'] = os.environ.get('URL_AUTH', 'localhost:8080')
    ENV['URL_FRONT'] = os.environ.get('URL_FRONT', 'localhost:3000')
    ENV['URL_NO_PROXY'] = os.environ.get('URL_NO_PROXY', 'localhost')
    ENV['URL_CHAT'] = os.environ.get('URL_CHAT', 'localhost:8088')

    ENV['ENTITY_UUID'] = os.environ.get('ENTITY_UUID', 'b20313a6-6b2d-43ce-be63-5f11b4deebe1')

    return ENV