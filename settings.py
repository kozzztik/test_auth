REDIS_SETTINGS = {
    'HOST': '127.0.0.1',
    'PORT': 6379,
    'DB': 9,
    'PREFIX': 'auth_'
}

SQL_SETTINGS = {'DB': 'sqlite:///:memory:'}
# SQL_SETTINGS = {'DB': 'mysql+mysqldb://root:123@localhost/test'}

# DB_BACKEND = 'db_backend.redis_backend.RedisBackend'
# DB_BACKEND_SETTINGS = REDIS_SETTINGS

DB_BACKEND = 'db_backend.sql_alchemy.SQLBackend'
DB_BACKEND_SETTINGS = SQL_SETTINGS

AUTH_BACKEND = {
    'simple': 'auth_backend.simple.SimpleAuthBackend',
    'facebook': 'auth_backend.facebook.FacebookAuthBackend'
}
