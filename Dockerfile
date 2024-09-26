# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install runtime dependencies and clean it
RUN set -ex \
    && RUN_DEPS=" \
    nginx \
    vim \
    usbutils \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $RUN_DEPS \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file to the container
COPY requirements.txt /app/

# Install the required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project to the container
COPY . /app/
RUN mkdir -p static

RUN python manage.py collectstatic --no-input --clear

COPY nginx/nginx_v2.conf /etc/nginx/nginx.conf


RUN chmod +x entrypoint.sh

# Expose the port the app runs on
EXPOSE 8000

# Run the Django development server (takes time but works)
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# does not work
# CMD ["gunicorn", "myapp.wsgi:application", "--bind", "0.0.0.0:8000"]

# below takes time but works
# CMD ["gunicorn", "myapp.wsgi:application", "--bind", "0.0.0.0:8000", "--worker-class", "gevent", "--workers", "3"]

# serve the app using nginx
ENTRYPOINT ["./entrypoint.sh"]