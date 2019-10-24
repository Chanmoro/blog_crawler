FROM python:3.7.3-stretch
MAINTAINER Chanmoro <kazuki.m777@gmail.com>

# Setup python environment using pipenv.
RUN pip install pipenv
COPY ./Pipfile ./Pipfile
COPY ./Pipfile.lock ./Pipfile.lock
RUN pipenv install --system
