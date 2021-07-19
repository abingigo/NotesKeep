import os

from flask import Flask

def create_app(test_config=None):
    app = Flask("personalinfomanager")
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'info.sqlite')
    )

    if test_config is not None:
        app.config.update(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import manager
    app.register_blueprint(manager.bp)

    from . import db 
    db.init_app(app)

    return app