# Use a slim Python image for smaller size
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
# This is done first to leverage Docker's layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
# Ensure your app directory structure matches:
# /app (WORKDIR)
# ├── app/
# │   ├── main.py
# │   ├── summarizer.py
# │   └── utils.py
# ├── static/
# │   └── style.css
# └── templates/
#     └── index.html
COPY app/ ./app/
COPY static/ ./static/
COPY templates/ ./templates/

# Expose the port that Uvicorn will run on
EXPOSE 8000

# Command to run the application using Uvicorn
# The --host 0.0.0.0 makes the server accessible from outside the container
# The --port 8000 matches the EXPOSE instruction
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
