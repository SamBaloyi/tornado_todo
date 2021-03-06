"""Main configuration for application."""
import logging
import os

from .views import (
    InfoView,
    ProfileView,
    RegistrationView,
    TaskListView,
    TaskView
)

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import options, define
from tornado_sqlalchemy import sessionmaker
from tornado.web import Application


define('port', default=8888, help='port to listen on')
factory = sessionmaker(os.environ.get(
    'DATABASE_URL',
    'postgres://localhost:5432/todo'
))


def main():
    """Construct and serve the application."""
    api_root = '/api/v1'
    app = Application([
        (api_root, InfoView),
        (api_root + r'/accounts', RegistrationView),
        (api_root + r'/accounts/([\w]+)', ProfileView),
        (api_root + r'/accounts/([\w]+)/tasks', TaskListView),
        (api_root + r'/accounts/([\w]+)/tasks/([\d]+)', TaskView),
    ],
        session_factory=factory,
        cookie_secret=os.environ.get('SESSION_SECRET', 'beefy'),
        **options.group_dict('application'),
    )
    http_server = HTTPServer(app)
    http_server.listen(options.port)
    logging.info('Listening on http://localhost:%d' % options.port)
    IOLoop.current().start()