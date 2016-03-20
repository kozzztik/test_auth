from base import BaseAuthDBBackend, UserAlreadyExist, UserNotExist
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker, mapper
from sqlalchemy.exc import IntegrityError


class BaseModel(object):

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)

    def __repr__(self):
        return '<%r %r>' % (self.__class__.__name__, self.id)

    def __getitem__(self, item):
        return getattr(self, item)


class SQLBackend(BaseAuthDBBackend):
    _token_class = None
    _engine = None
    _metadata = None
    _models = None

    def _init_connection(self, settings):
        connect_str = settings['DB']
        self._engine = create_engine(connect_str, convert_unicode=True)
        self._metadata = MetaData(bind=self._engine)
        self._models = {}
        return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self._engine))

    def get_user(self, auth_type, user_id):
        model_class = self._models[auth_type]
        user = model_class.query.filter(model_class.user_id == user_id).first()
        if not user:
            raise UserNotExist()
        return user

    def add_user(self, auth_type, user_id, **data):
        model_class = self._models[auth_type]
        user = model_class(user_id=user_id, **data)
        self.connection.add(user)
        try:
            self.connection.commit()
        except IntegrityError:
            self.connection.rollback()
            raise UserAlreadyExist()

    def init_db(self):
        self._token_class = type('TokensModel', (BaseModel,), {'query': self.connection.query_property()})
        token_table = Table('tokens', self._metadata,
                            Column('id', Integer, primary_key=True),
                            Column('token', String(120)),
                            Column('backend', String(120)),
                            Column('value', String(120))
                            )
        mapper(self._token_class, token_table)
        self._metadata.create_all()

    def register_auth_backend(self, auth_backend):
        model_class = type(auth_backend.name + 'Model', (BaseModel,), {'query': self.connection.query_property()})
        backend_table = Table(auth_backend.name, self._metadata,
                              Column('id', Integer, primary_key=True),
                              Column('user_id', String(50), unique=True),
                              *[Column(field, String(120)) for field in auth_backend.fields]
                              )
        mapper(model_class, backend_table)
        self._models[auth_backend.name] = model_class
        auth_backend.model = model_class

    def get_auth_token(self, auth_type, token):
        obj = self._token_class.query.filter(self._token_class.token == token, self._token_class.backend == auth_type
                                             ).first()
        return obj.value if obj else None

    def set_auth_token(self, auth_type, token, value):
        obj = self._token_class.query.filter(self._token_class.token == token,
                                             self._token_class.backend == auth_type,
                                             ).first()
        if not obj:
            obj = self._token_class(backend=auth_type, token=token)
        obj.value = value
        self.connection.add(obj)
        self.connection.commit()
