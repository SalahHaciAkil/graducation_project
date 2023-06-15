# Use the official Python image as the base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app's source code to the working directory
COPY . .

# Expose the port used by the Django app
EXPOSE 8000

# Run the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]