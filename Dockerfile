# Use the official Python image 
FROM python:3.10

# Set the working directory in the container to /app
WORKDIR /app

# Use ARG to accept the API key as a build argument
ARG API_KEY

# Use ENV to set the API key as an environment variable
ENV API_KEY=$API_KEY

# Copy the poetry files
COPY pyproject.toml poetry.lock /app/

# Install poetry
RUN pip install poetry

# Install project dependencies
RUN poetry lock
RUN poetry install

# Copy the rest of the project
COPY . .

# Extract data for app
RUN poetry run ploomber build

# Expose the port that the app runs on
EXPOSE 8000

# Execute the script when the container starts
CMD ["poetry", "run", "uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]
