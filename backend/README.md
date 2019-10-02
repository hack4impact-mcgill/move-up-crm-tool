# How to Run

First off, make sure to create a virtual environment on your machine. A virtual environment can be created with either `virtualenv` (python 2) or `venv` (python 3). For `venv`:

```
python3 -m venv env

source env/bin/activate
```

The second line activates the virtual environment, and you can type `deactivate` to exit the environment.

To install dependencies from a `requirements.txt` file, do this:

```
pip install -r /path/to/requirements.txt
```

To see all installed modules:

```
pip list
```

## Flask App Folder Structure

```
|-app-name/
	|-backend/
		|-tests/
		|-requirements.txt
		|-config.py # define various configurations
		|-manage.py # script for running the application
		|-app/
			|-main/
				|-__init_.py # set up Blueprint 'main' here
				|-views.py # routes for main Blueprint here
				|-errors.py # set up error routes
			|-other_blueprint/
				|-__init_.py # set up Blueprint 'other_blueprint' here
				|-views.py # routes for other_blueprint Blueprint here
				|-errors.py # set up error routes
			|-__init__.py # create_app factory function goes here
	|-frontend/
		|-...
```

To run a Blueprint-based app, run `python manage.py runserver`. To run all tests, run `python manage.py test`.
