# Use a minimal Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the project files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables (optional but clean)
ENV PYTHONUNBUFFERED=1

# Run the main script to create and populate the SQLite DB
CMD ["python", "main.py"]
