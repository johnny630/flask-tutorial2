# python core
import os

# flask relative
from flask import Flask, g
from flask.cli import with_appcontext

# extensions
import click
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_migrate import Migrate, upgrade, migrate


dotenv_path = os.path.join(os.path.dirname(__file__), '.flaskenv')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path, override=True)

db = SQLAlchemy()
migrates = Migrate()

def create_app():
    app = Flask(__name__)
    config_name = os.getenv('FLASK_ENV')
    
    from .config.config import config
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)

    app.cli.add_command(test_command)

    @app.route('/')
    def index():
        return 'index'

    return app

def register_extensions(app):
    db.init_app(app)
    migrates.init_app(app, db)

def register_blueprints(app):
    from .views.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

@click.command('test-command')
@with_appcontext
def test_command():
    """Clear the existing data and create new tables."""
    click.echo('Initialized the databash.')
