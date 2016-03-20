from .base import BaseAuthBackend, InvalidCredentials
from db_backend.base import UserNotExist, UserAlreadyExist


class FacebookAuthBackend(BaseAuthBackend):
    """
    Facebook auth backend by facebook tokens
    """
    fields = ['email']

    def sign_in(self, facebook_token):
        """
        Sign user in system
        :param str facebook_token: Facebook auth token
        :return:
        """
        user_id = self.get_auth_token(facebook_token)
        if not user_id:
            raise InvalidCredentials()
        try:
            user = self._get_user(user_id)
        except UserNotExist:
            raise InvalidCredentials()
        return user

    def sign_up(self, email, facebook_id, facebook_token):
        """
        Register user in system
        :param str email: User email
        :param str facebook_id: Facebook user id
        :param str facebook_token: Facebook auth token
        :return:
        """
        try:
            self._add_user(facebook_id, email=email)
        except UserAlreadyExist:
            pass
        self.set_auth_token(facebook_token, facebook_id)
