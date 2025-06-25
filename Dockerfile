#build image
FROM python:3.13-slim

# Run a shell command inside the container "During docker build"
# Make the /app folder to store your application files.
# WORKDIR like a cd, Move into that folder inside container
WORKDIR /app

# Set env variable
# No __pycache__ directories are created.
ENV PYTHONDONTWRITEBYTECODE=1
#Output is sent directly to the terminal or Docker logs in real time without stored
#error go to the cmd
ENV PYTHONUNBUFFERED=1

# Upgrade pip
RUN pip3 install --upgrade pip
# copy dependencies from your local machine into the /app/ folder
 # Executes a shell command inside the Docker image during build.
# --no-cache-dir to prevents pip from saving downloaded in a cache.
COPY requirements.txt  .

COPY . .
RUN mkdir -p /app/staticfiles

RUN pip3 install --no-cache-dir -r requirements.txt
RUN python manage.py collectstatic --noinput

EXPOSE 8000
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]