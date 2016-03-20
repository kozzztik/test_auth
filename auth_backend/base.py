class InvalidCredentials(Exception):
    pass


class BaseAuthBackend(object):
    fields = []

    def __init__(self, name, db_backend):
        """

        :param str name: Auth backend name
        :param db_backend.base.BaseAuthDBBackend db_backend: db backend object
        :return:
        """
        self.name = name
        self.db_backend = db_backend
        db_backend.register_auth_backend(self)

    def _get_user(self, user_id):
        """
        Get user profile data
        :param str user_id:
        :return: dict
        """
        return self.db_backend.get_user(self.name, user_id)

    def _add_user(self, user_id, **data):
        """
        Add user to DB
        :param str user_id: user id
        :param dict data: user profile data
        :return:
        """
        self.db_backend.add_user(self.name, user_id, **data)

    def set_auth_token(self, token, value):
        """
        Set temp auth token
        :param str token: token name
        :param str value: token value
        :return:
        """
        self.db_backend.set_auth_token(self.name, token, value)

    def get_auth_token(self, token):
        """
        Get temp auth token value
        :param token:
        :return:
        """
        return self.db_backend.get_auth_token(self.name, token)

    def sign_in(self, **kwargs):
        raise NotImplementedError()

    def sign_up(self, **kwargs):
        raise NotImplementedError()
