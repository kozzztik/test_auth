from flask import request, current_app, jsonify
from flask.views import View
from importlib import import_module


def import_class(dotted_path):
    module_path, class_name = dotted_path.rsplit('.', 1)
    module = import_module(module_path)
    return getattr(module, class_name)


class AuthBackend(object):
    def __init__(self, app=None):
        db_backend_class = import_class(app.config.get('DB_BACKEND', 'db_backend.redis_backend.RedisBackend'))
        db_backend = db_backend_class(app.config.get('DB_BACKEND_SETTINGS', {}))
        auth_backend = {}
        for name, class_path in app.config.get('AUTH_BACKEND', {}).items():
            auth_backend_class = import_class(class_path)
            auth_backend[name] = auth_backend_class(name, db_backend)
        if not auth_backend:
            raise ValueError('Auth backend not configured')
        app.auth_backend = auth_backend
        app.auth_db = db_backend
        db_backend.init_db()


class BaseAuthView(View):
    methods = ['POST']
    backend_func_name = None

    def dispatch_request(self):
        def error(s):
            return jsonify(error=s), 400
        kwargs = {key: value for key, value in request.values.items()}
        auth_backend_name = kwargs.pop('type', None)
        auth_backend = getattr(current_app, 'auth_backend', None)
        if not auth_backend:
            return error('Auth backend app not started')
        if (not auth_backend_name) or (auth_backend_name not in auth_backend):
            return error('backend type is invalid')
        backend = auth_backend[auth_backend_name]
        func = getattr(backend, self.backend_func_name, None)
        if not func:
            return error('Bad backend')
        try:
            func(**kwargs)
        except Exception, e:
            return error(str(e))
        return jsonify({})


class SignupView(BaseAuthView):
    backend_func_name = 'sign_up'


class SigninView(BaseAuthView):
    backend_func_name = 'sign_in'
