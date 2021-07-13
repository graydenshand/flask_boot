from .base_installer import FlaskExtInstaller
from .flask_sqlalchemy import FlaskSQLAlchemyInstaller
import subprocess
import shutil
import click
import os


class FlaskMigrateInstaller(FlaskExtInstaller):
    package_name = "Flask-Migrate"
    dependencies = [FlaskSQLAlchemyInstaller]
    imports = ["from flask_migrate import Migrate"]
    inits = ['migrate = Migrate(db, directory="src/migrations")']
    attachments = ["migrate.init_app(app)"]

    @classmethod
    def install(cls):
        super().install()
        subprocess.run("source venv/bin/activate && flask db init", shell=True)
        click.secho("Initialized migrations directory at `src/migrations`", fg="green")

    @classmethod
    def uninstall(cls):
        super().uninstall()
        if os.path.exists(os.path.join("src", "migrations")):
            shutil.rmtree(os.path.join("src", "migrations"))
            click.secho(f"Destroyed {os.path.join('src', 'migrations')}", fg="red")

    @classmethod
    def verify(cls, verbose=False):
        if not os.path.exists(os.path.join("src", "migrations")):
            if verbose:
                click.secho(
                    f"Package Verification Error: Flask-Migrate `migrations` directory doesn't exist",
                    fg="red",
                )
            return False
        else:
            return super().verify(verbose)
