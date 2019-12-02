#!/usr/bin/env python
import os

from flask_script import Manager

# Import settings from .env file. Must define FLASK_CONFIG
if os.path.exists(".env"):
    print("Importing environment from .env file")
    for line in open(".env"):
        var = line.strip().split("=")
        if len(var) == 2:
            os.environ[var[0]] = var[1]

from app import create_app

app = create_app(os.getenv("FLASK_CONFIG") or "default")
manager = Manager(app)


@manager.command
def test():
    """Run the unit tests."""
    import unittest

    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == "__main__":
    manager.run()
