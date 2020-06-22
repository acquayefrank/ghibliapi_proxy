# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image, specifically the python 3.6 version
FROM python:3.8

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir code

# Set the working directory to code
WORKDIR code

# Copy the current directory contents into the container at code
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
