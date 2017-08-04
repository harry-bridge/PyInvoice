# Start with ARM base image
FROM resin/raspberrypi3-python:3.6.1

#Env vars
ENV RUN_POSTGRES 1

# Create directorues
RUN mkdir /code
WORKDIR /code
COPY . /code

# Install requirements
RUN pip install -U pip
RUN pip install --no-cache-dir -r requirements.txt

# Collect our static media.
RUN python /code/manage.py collectstatic --noinput

CMD ["/code/bin/docker_run.sh"]
