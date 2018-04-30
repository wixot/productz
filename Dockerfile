#FIXME dash export vue

FROM ubuntu:16.04
MAINTAINER wixot <hello@wixot.com>

# Never prompts the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

ARG AIRFLOW_VERSION=1.9.0
ARG AIRFLOW_HOME=/root/airflow


RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-venv python3-pip build-essential apt-utils

RUN apt-get install -y libmysqlclient-dev
RUN apt-get install -y supervisor
# Set the working directory to /pdc
WORKDIR /pdc

# Copy the current directory contents into the container at /pdc
ADD . /pdc

RUN python3 -m venv .venv

# Install any needed packages specified in requirements.txt
RUN pip3 install --trusted-host pypi.python.org -U pip
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt
RUN pip3 install --trusted-host pypi.python.org apache-airflow[devel]==$AIRFLOW_VERSION
RUN .venv/bin/pip install --trusted-host pypi.python.org -U pip
RUN .venv/bin/pip install --trusted-host pypi.python.org -r requirements.txt
# Define environment variable
ENV PYTHONPATH /pdc:$PYTHONPATH

RUN airflow initdb
RUN cp -R dags/ /root/airflow

RUN ls /root/airflow/dags

RUN airflow resetdb -y

ADD scripts/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Make port 80 available to the world outside this container
EXPOSE 5000 8080


# Run app.py when the container launches
ENTRYPOINT ["/usr/bin/supervisord"]
