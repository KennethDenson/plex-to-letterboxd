# Use an official lightweight Python image
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Install required Python dependencies
RUN pip install plexapi pandas schedule  # Removed cron and croniter

# Copy the Python script into the container
COPY export_plex.py .

# Set the default command to run the script
CMD ["python3", "export_plex.py"]
