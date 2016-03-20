import unittest
import app


class AuthBackendTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()

    def _sign_in(self, **kwargs):
        return self.app.post('/auth/signin/', data=dict(**kwargs)).status_code == 200

    def _sign_up(self, **kwargs):
        return self.app.post('/auth/signup/', data=dict(**kwargs)).status_code == 200

    def test_simple_signup(self):
        # Auth without password fails
        assert not self._sign_up(type='simple', email='test@test.com')
        # Auth works
        assert self._sign_up(type='simple', email='test@test.com', password='testpass')
        # Cant register twice
        assert not self._sign_up(type='simple', email='test@test.com', password='testpass')
        # Can login
        assert self._sign_in(type='simple', email='test@test.com', password='testpass')
        # Cant login with wrong pass
        assert not self._sign_in(type='simple', email='test@test.com', password='testpass2')

    def test_facebook_signup(self):
        # Auth without token fails
        assert not self._sign_up(type='facebook', email='test@test.com', facebook_id='fid')
        # Auth works
        assert self._sign_up(type='facebook', email='test@test.com', facebook_id='fid', facebook_token='ftid')
        # Can login
        assert self._sign_in(type='facebook', facebook_token='ftid')
        # Can register facebook id twice with different token
        assert self._sign_up(type='facebook', email='test@test.com', facebook_id='fid', facebook_token='ftid2')
        # Can login with new token
        assert self._sign_in(type='facebook', facebook_token='ftid2')
        # Cant login with bad token
        assert not self._sign_in(type='facebook', facebook_token='ftid3')
        # Cant login by faceook id without token
        assert not self._sign_in(type='facebook', facebook_id='fid')


if __name__ == '__main__':
    unittest.main()