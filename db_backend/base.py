class UserAlreadyExist(Exception):
    pass


class UserNotExist(Exception):
    pass


class BaseAuthDBBackend(object):

    def __init__(self, settings):
        """
        Init backend with settings and create connection
        :param dict settings: DB backend settings
        :return:
        """
        self.connection = self._init_connection(settings)

    def _init_connection(self, settings):
        """
        Init connection to backend
        :param dict settings: DB backend settings
        :return:
        """
        raise NotImplementedError()

    def init_db(self):
        """
        Init backend database structure
        :return:
        """
        raise NotImplementedError()

    def get_user(self, auth_type, user_id):
        """
        Get user info from DB
        :param str auth_type: Auth backend type name
        :param str user_id: User ID in auth backend
        :return: dict
        """
        raise NotImplementedError()

    def add_user(self, auth_type, user_id, **data):
        """
        Add user to DB
        :param str auth_type: Auth backend type name
        :param str user_id: User ID in auth backend
        :param dict data: User profile data
        :return: dict
        """
        raise NotImplementedError()

    def get_auth_token(self, auth_type, token):
        """
        Get temporary auth token from DB
        :param str auth_type: Auth backend type name
        :param str token: token name
        :return:
        """
        raise NotImplementedError()

    def set_auth_token(self, auth_type, token, value):
        """
        Sets temp auth token
        :param str auth_type: Auth backend type name
        :param str token: Token name
        :param str value: Value of token
        :return:
        """
        raise NotImplementedError()

    def register_auth_backend(self, auth_backend):
        """
        Register auth backend in DB for proper mapping
        :param auth_backend.base.BaseAuthBackend auth_backend: Auth backend
        :return:
        """
        raise NotImplementedError()
