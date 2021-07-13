from flask_batteries import new
from click.testing import CliRunner
from ..conf_tests import cli, app
import os
from pkg_resources import resource_filename
import re
import subprocess
import pathspec


def test_new_doesnt_fail(cli):
    result = cli.invoke(new)
    assert result.exit_code == 0


def test_new_creates_all_resources_in_template_directory(cli, app):
    # Walk the app template and verify every file and directory was copied
    with open(resource_filename("flask_batteries", "template/.gitignore"), "r") as f:
        ignore_spec = pathspec.PathSpec.from_lines("gitwildmatch", f)
    ignore_matches = list(
        ignore_spec.match_tree(resource_filename("flask_batteries", "template"))
    )
    for dirpath, dirs, files in os.walk(
        resource_filename("flask_batteries", "template")
    ):
        pattern = r"template[\/]*(.*)"
        match = re.search(pattern, dirpath)
        path = match.group(1)
        for d in dirs:
            if d != "__pycache__":
                resource = os.path.join(path, d).lstrip("\\") if path else d
                assert os.path.exists(resource)
        for f in files:
            resource = os.path.join(path, f).lstrip("\\") if path else f
            if resource not in ignore_matches:
                assert os.path.exists(resource)


def test_generated_app_passes_all_generated_tests(cli, app):
    # Run the generated app's test suite and verify exit code is 0
    if os.name != "nt":
        run_tests = subprocess.run("source venv/bin/activate && pytest", shell=True)
    else:
        run_tests = subprocess.run("venv\\Scripts\\activate && pytest", shell=True)
    assert run_tests.returncode == 0, run_tests.stdout


def test_new_with_path_to_venv_option_doesnt_fail():
    runner = CliRunner()
    with runner.isolated_filesystem():
        os.mkdir("app")
        os.chdir("app")
        subprocess.run("python -m venv .venv", shell=True)
        result = runner.invoke(new, ["--path-to-venv", ".venv"])
        assert result.exit_code == 0
