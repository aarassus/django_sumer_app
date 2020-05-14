FROM python:3.7 

# Permet à Python d'afficher tout ce qui est imprimé dans l'application plutôt que de le mettre en mémoire tampon.
ENV PYTHONUNBUFFERED 1

# Création of the workdir
RUN mkdir /code
WORKDIR /code

# Add requirements.txt file to container
ADD requirements.txt /code/

# Install requirements
RUN pip install --upgrade pip
RUN pip install torch
RUN pip install torchvision
RUN pip install -r /code/requirements.txt

# Add the current directory(the web folder) to Docker container
ADD . /code/
