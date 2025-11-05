from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_caching import Cache
from celery import Celery


db = SQLAlchemy()
login_manager = LoginManager()
cache = Cache()


def make_celery(create_app):
    try:
        # Try creating a Flask app normally
        flask_app = create_app()
    except Exception:
        # If app cannot be created yet (e.g. circular import), fall back to None
        flask_app = None

    # Create the Celery app with safe defaults
    celery_app = Celery(
        __name__,
        broker="redis://localhost:6379/0",
        backend="redis://localhost:6379/0",
    )

    # If the Flask app was created successfully, update config and context
    if flask_app:
        celery_app.conf.update(flask_app.config)

        class ContextTask(celery_app.Task):
            def __call__(self, *args, **kwargs):
                with flask_app.app_context():
                    return self.run(*args, **kwargs)

        celery_app.Task = ContextTask

    return celery_app
