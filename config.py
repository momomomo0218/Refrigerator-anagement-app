import os
if os.environ.get('MY_NAME') == 'makaniaizu':
    import psycopg2

# 開発用設定
if os.environ.get('FLASK_ENV') == 'production':
    SECRET_KEY = os.environ['FLASK_SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1)
else:
    DEBUG = True
    # TESTING = True
    if os.environ.get('MY_NAME') == 'makaniaizu':
        SQLALCHEMY_DATABASE_URI = 'postgresql://makaniaizu:password@localhost/test'
        SECRET_KEY = os.environ['FLASK_SECRET_KEY']
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
        SECRET_KEY = 'my_secret_key'

