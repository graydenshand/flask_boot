#!/opt/homebrew/bin/python3
import os
import sys
import re
from jinja2 import Environment, PackageLoader, select_autoescape
from datetime import datetime
import subprocess
import click
from pkg_resources import resource_filename
import shutil
import pathspec

@click.command(help="Generate a new flask_boot app")
@click.argument("name")
def new(name):
    print("Generating new app named: %s" % name)
    env = Environment(
        loader=PackageLoader("flask_boot", "template"), autoescape=select_autoescape()
    )

    def render_template(filename, **params):
        template = env.get_template(filename)
        return template.render(**params)

    def copy_template(filename, **params):
        if "src/assets/images" not in filename:
            with open(filename, "w+") as f:
                f.write(render_template(filename, **params))
        else:
            # Copy image files directly
            shutil.copyfile(resource_filename("flask_boot", f"template/{filename}"), filename)
        return

    def set_env_vars(skip_check=False, **kwargs):
        # Add an environment variable to venv/bin/activate
        if skip_check:
            with open("venv/bin/activate", "a") as f:
                for key, val in kwargs.items():
                    f.write(f"export {key}={val}\n")
            return
        else:
            with open("venv/bin/activate", "r") as f:
                # Get existing file content
                body = f.read()

            with open("venv/bin/activate", "w") as f:
                # If key is already specified, remove it
                for key, val in kwargs.items():
                    regex = f"export {key}={val}\n"
                    body = re.sub(regex, "", body) + f"export {key}={val}\n"
                    f.write(body)
            return

    # Create empty directory and set it as current working directory
    os.mkdir(name)
    os.chdir(name)

    with open(resource_filename("flask_boot", "template/.gitignore"), 'r') as f:
        ignore_spec = pathspec.PathSpec.from_lines('gitwildmatch', f)
    ignore_matches = list(ignore_spec.match_tree(resource_filename("flask_boot", "template")))
    # Walk the app template and copy every file and directory
    for dirpath, dirs, files in os.walk(resource_filename("flask_boot", "template")):
        pattern = r"template\/*(.*)"
        match = re.search(pattern, dirpath)
        path = match.group(1)
        for d in dirs:
            if d != '__pycache__':
                resource = path + "/" + d if path else d
                os.mkdir(resource)
        for f in files:
            resource = path + "/" + f if path else f
            if resource not in ignore_matches:
                copy_template(resource, name=name)

    # Initialize git repo
    subprocess.run(["git", "init", "--initial-branch=main"])
    # Initialize virtual env
    subprocess.run(["python3", "-m", "venv", "venv"])
    ## Install requirements
    requirements = ["flask", "pytest", "requests"]
    subprocess.run([f"venv/bin/pip", "install"] + requirements)
    ## Set default environment variables
    envs = {
        "FLASK_APP": "main.py",
        "FLASK_ENV": "development",
        "SECRET_KEY": os.urandom(24).hex(),
    }
    set_env_vars(skip_check=True, **envs)
