from .base import BaseAuthBackend, InvalidCredentials
from db_backend.base import UserNotExist
import hashlib


class SimpleAuthBackend(BaseAuthBackend):
    """
    Simple auth backend by email and password.
    Password is simple hashed.
    """
    fields = ['password']

    @staticmethod
    def _hash_pass(user_id, password):
        """
        Get hash of user password
        :param str user_id: User id
        :param str password: User password
        :return:
        """
        return hashlib.sha1(user_id + password).hexdigest()

    def sign_in(self, email, password):
        """
        Sign user in system
        :param str email: User email
        :param str password: User password
        :return:
        """
        try:
            user = self._get_user(email)
        except UserNotExist:
            raise InvalidCredentials()
        user_password_data = user['password']
        if self._hash_pass(email, password) != user_password_data:
            raise InvalidCredentials()
        return user

    def sign_up(self, email, password):
        """
        Register user in system
        :param str email: User email
        :param str password: User password
        :return:
        """
        self._add_user(email, password=self._hash_pass(email, password))
