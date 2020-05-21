import gunicorn.app.base

from readrr_api import create_app
from readrr_api.route_tools.recommender import tokenize

# class is a workaround for missing tokenize attribute in tfidf
# container runs gunicorn from a python file as an ENTRYPOINT
# in order to access variable on module __main__


class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == '__main__':
    options = {
        'bind': '%s:%s' % ('0.0.0.0', '8000')
    }
    StandaloneApplication(create_app(), options).run()
