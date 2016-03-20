from base import BaseAuthDBBackend, UserAlreadyExist, UserNotExist
from redis import Redis


class RedisBackend(BaseAuthDBBackend):
    _models = None

    def _init_connection(self, settings):
        self.prefix = settings.get('PREFIX', '')
        self.token_expire = settings.get('TOKEN_EXPIRE', 0)
        self._models = {}
        return Redis(host=settings.get('HOST', 'localhost'), port=settings.get('PORT', 6379), db=settings.get('DB', 0))

    def user_key(self, auth_type, user_id):
        return "%s%s:%s" % (self.prefix, auth_type, user_id)

    def get_user(self, auth_type, user_id):
        fields = self._models[auth_type]
        key = self.user_key(auth_type, user_id)
        pipe = self.connection.pipeline()
        pipe.exists(key)
        pipe.hmget(self.user_key(auth_type, user_id), fields)
        exist, data = pipe.execute()
        if not exist:
            raise UserNotExist()
        return {name: value for name, value in zip(fields, data)}

    def add_user(self, auth_type, user_id, **data):
        fields = self._models[auth_type]
        key = self.user_key(auth_type, user_id)
        pipe = self.connection.pipeline()
        for field in fields:
            pipe.hsetnx(key, field, data.get(field, None))
        result = pipe.execute()
        if not all(result):
            raise UserAlreadyExist()

    def init_db(self):
        self.connection.flushdb()

    def token_key(self, auth_type, token):
        return "%s%s_token:%s" % (self.prefix, auth_type, token)

    def get_auth_token(self, auth_type, token):
        return self.connection.get(self.token_key(auth_type, token))

    def set_auth_token(self, auth_type, token, value):
        self.connection.set(self.token_key(auth_type, token), value, ex=self.token_expire or False)

    def register_auth_backend(self, auth_backend):
        self._models[auth_backend.name] = auth_backend.fields

