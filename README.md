*\~work in progress\~*

# Flask-Batteries

An opinionated command line tool for bootstrapping Flask applications with less boiler-plate code.

This package does two things:
1) Asserts a sensible project structure for larger applications.
2) Supplies new commands to the Flask cli for managing this project structure.


## Usage


Install Flask-Batteries through pip:
```bash
pip install flask-batteries
```

This will add a command, `flask new`, to your Flask cli. To create a new app named "blog", enter:
```bash
flask new blog
```

A new Flask app will be created in the `./blog` directory.

To run the app:
```bash
cd blog
# Install Node packages
npm install
# Activate virtual environment and run the app
source venv/bin/activate
flask run
```

Open up https://127.0.0.1:5000/ in your browser and you should see your app running.

### Webpack
By default, the generated app uses Webpack to bundle static assets. Use the `flask build` command to compile the assets and generate a 'static' folder. This command should be run in your build pipeline when pushing to production.

When running the app in development mode, the static assets will be regenerated every time the debug server restarts. This can be somewhat slow. Webpack has a development server that makes this process much faster. You can run the Webpack dev server in a separate terminal window by using the `flask watch` command. 

The Webpack dev server will serve your assets on a different port. So, when it is running, we need to pull static assets from `localhost:3000/static`, and when it's not running we need to pull static assets from `localhost:5000/static`. The `static_url_for(filename)` function handles this logic and will route requests to the webpack server only if it is running. This function is automatically passed to all of your Jinja2 templates, and can be imported elsewhere via `from flask_batteries import static_url_for`.

If you don't want to use Webpack, you can use a standard 'static' folder by passing the `--skip-webpack` option to `flask new`.


### Installing extensions
Flask-Batteries knows how to install common Flask extensions. 

For example, to use Flask-WTF, you can simply call:
```bash
flask install wtf
```
This will add Flask-WTF to your project requirements, and create a new 'forms' folder in your project to store forms. 

To reverse the installation, call:
```bash
flask uninstall wtf
```

Each installer is unique, and some require additional configuration (which will be reported in the output of the install command).

To see the full list of supported extensions, call:
```bash
flask install
```

### Generating files
Flask-Batteries will generate files for you to help keep your project organized.

For example, if you wanted to create a new route "/sign-up". You could call:
```bash
flask generate route sign_up
```

*Note: use snake_case for route names*

This will:
* Create a file named `src/routes/sign_up.py`, and include a boiler plate route definition.
* Create a template named `src/templates/sign_up.html`, and include some sample content. 
* Create a file named `test/routes/test_sign_up.py`, and include a sample test. 
* Map the generated route to the `/sign-up` endpoint. 

Fire up your development server and head to localhost:5000/sign-up to see the generated page. 

You can also specify one or many custom url_rules to apply to the route. Eg:
```bash
flask generate route sign_up /sign-up /register
```

This will map your generated route to both the `/sign-up` and the `/register` endpoints. 

To reverse this action, call:
```bash
flask destroy route sign_up
```

Finally, to see the full list of generators, call:
```bash
flask generate
```

### Virtual Environments
By default, the `flask new <name>` command will generate a virtual environment in the `venv` directory of the generated project. 

You can change the location of the virtual environment by passing the `--path-to-venv` option to the `flask new` command. Eg:
```bash
flask new --path-to-venv=.vir_env blog
```

### Flask new in current directory
You can also call the `flask new` command without the `name` argument to generate an app in your current working directory. 

### Git
The `flask new` command sets up a git repository for the generated project. 

By default, it uses 'main' as the name of the primary branch. You can override this by passing the `--git-initial-branch` option to the `flask new` command. Eg:
```bash
flask new --git-initial-branch=master blog
```

### Method Views
The routes generated by Flask-Batteries use Flask's [MethodView](https://flask.palletsprojects.com/en/2.0.x/views/#method-based-dispatching) class.

All URL rules are located in the `register_routes()` function of the `src/routes/__init__.py` file. 


### Testing
Flask-Batteries includes a testing suite in the `test/` directory of the generated project. 

The testing suite runs on [pytest](https://docs.pytest.org/en/6.2.x/) and [uses a test client as described in the flask docs](https://flask.palletsprojects.com/en/2.0.x/testing/).

To run the tests, call `pytest` from the root directory of the generated project.

## Development
Thanks for your interest in contributing to this project!

Pull requests and feedback on the project are welcome. 

Clone this repository with:
```bash
git clone https://github.com/graydenshand/flask-batteries.git
```

Set up a virtual environment and install the package requirements:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Tests are run with [tox](https://tox.readthedocs.io/en/latest/) against python 3.9. 

To run the tests, simply call `tox` from the root directory. 

## Roadmap
### V 1.0.0
Commands:
* ✅ `flask new`: generate a new Flask-Batteries app
* ✅ `flask webpack build`: build static assets with Webpack
* ✅ `flask webpack watch`: build and watch static assets with Webpack
* ✅ `flask (un)install sqlalchemy`: (un)install Flask-SQLAlchemy
* ✅ `flask (un)install migrate`: (un)install Flask-Migrate
* ✅ `flask (un)install wtf`: (un)install Flask-WTF
* ❌ `flask (un)install uploads`: (un)install Flask-Uploads
* ✅ `flask (un)install babel`: (un)install Flask-Babel
* ✅ `flask (un)install login`: (un)install Flask-Login
* ❌ `flask (un)install principal`: (un)install Flask-Mail
* ✅ `flask (un)install mail`: (un)install Flask-Mail
* ✅ `flask (un)install talisman`: (un)install Flask-Talisman
* ❌ `flask (un)install cors`: (un)install Flask-CORS
* ❌ `flask (un)install security`: (un)install Flask-Security
* ❌ `flask (un)install sessions`: (un)install Flask-Sessions
* ❌ `flask (un)install restful`: (un)install Flask-Restful
* ❌ `flask (un)install bootstrap`: (un)install Flask-Bootstrap
* ✅ `flask generate/destroy route`: generate/destroy a route, template, and test
* ✅ `flask generate/destroy model`: generate/destroy a Flask-SQLAlchemy model, a new test file, and Flask-Marshmallow schema.
* ❌ `flask generate/destroy form`: generates a Flask-WTF form, and imports it to the `forms/__init__.py` file. 
* ✅ `flask generate/destroy stylesheet`: generates a new .scss stylesheet and imports it to the `assets/stylesheets/styles.scss` file. If webpack is not being used, creates a new .css stylesheet. 
* ✅ `flask translate init`: Initialize a new translation language (Flask-Babel)
* ✅ `flask translate update`: Update all translations (Flask-Babel)
* ✅ `flask translate compile`: Compile all translations (Flask-Babel)

Other featutes:
* ✅ Allow skipping of webpack, and using a simple 'static' folder: `flask new --skip-webpack`. 
* ✅ Allow skipping of Flask-SQLAlchemy and Flask-Migrate: `flask new app --skip-db`
* ✅ Allow creating a primary git branch other than `main`: `flask new app --git-initial-branch master`
* ✅ Allow custom url_rules specification when generating routes:  `flask generate route sign_up /sign-up /register /join` 
