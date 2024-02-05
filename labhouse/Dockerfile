# Use an official Python runtime as the base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

RUN apt-get update -y
RUN apt-get install python3-psycopg2

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Update pipRUN  pip install --upgrade pip
RUN pip install --upgrade pip

# Install the project dependencies
RUN pip install -r requirements.txt

# Copy the project code to the working directory
COPY . .

#RUN python manage.py makemigrations
#RUN python manage.py migrate --settings=labhouse.settings

# Expose the default Django port (change it if necessary)
EXPOSE 8000

# Run the Django development server when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
