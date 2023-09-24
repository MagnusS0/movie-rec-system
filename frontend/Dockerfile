# Use the official Python image 
FROM python:3.10

# Set the working directory in the container to /app
WORKDIR /frontend

# Copy the poetry files
COPY pyproject.toml poetry.lock /frontend/

# Install poetry
RUN pip install poetry

# Install the dependencies globally within the container.
RUN poetry config virtualenvs.create false

# Install project dependencies
RUN poetry lock
RUN poetry install

# Copy the frontend application file to the working directory
COPY frontend_app.py .

# Expose the port the app runs on
EXPOSE 8501

# Execute the script when the container starts
CMD ["streamlit", "run", "frontend_app.py"]