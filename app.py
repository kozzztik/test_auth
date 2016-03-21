from flask import Flask
from auth import SignupView, SigninView, AuthBackend

app = Flask(__name__.split('.')[0], static_folder=None, static_url_path=None)

app.config.from_object('settings')
app.config.from_envvar('PRODUCTION_SETTINGS', silent=True)

AuthBackend(app)

app.add_url_rule('/auth/signup/', view_func=SignupView.as_view('signup'))
app.add_url_rule('/auth/signin/', view_func=SigninView.as_view('signin'))


if __name__ == '__main__':
    import os
    app.run(host=os.environ.get('HOST', 'localhost'), port=8000, debug=True, threaded=False)
