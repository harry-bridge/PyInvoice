# Start with a Python image.
FROM python:2.7

# Some stuff that everyone has been copy-pasting
# since the dawn of time.
ENV PYTHONUNBUFFERED 1

# Install some necessary things.
RUN apt-get update
#RUN apt-get install -y swig libssl-dev dpkg-dev netcat

# Copy all our files into the image.
RUN mkdir /code
WORKDIR /code
COPY . /code/

# Install our requirements.
RUN pip install -U pip
RUN pip install -Ur requirements.txt

# Collect our static media.
RUN python /code/manage.py collectstatic --noinput

# Specify the command to run when the image is run.
CMD ["/code/bin/docker_run.sh"]
