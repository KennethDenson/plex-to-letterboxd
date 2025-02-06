# Use an official lightweight Python image
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Install required dependencies and cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*
RUN pip install plexapi pandas croniter

# Copy the Python script into the container
COPY export_plex.py .

# Copy the cron job setup script
COPY start-cron.sh .

# Give execution permissions
RUN chmod +x start-cron.sh

# Start the cron daemon
CMD ["sh", "./start-cron.sh"]
