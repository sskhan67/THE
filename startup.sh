#! /bin/bash

export PYTHONUNBUFFERED=1
export FLASK_APP=wsgi.py
export FLASK_ENV=production
export SECRET_KEY=e9a9f6fa5fac
export SQLALCHEMY_DATABASE_URI=sqlite:///db.sqlite?check_same_thread?=False


python wsgi.py
