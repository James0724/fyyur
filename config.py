import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:kacosdfol@localhost:5432/fyyurdb'
SQLALCHEMY_TRACK_MODIFICATIONS = False