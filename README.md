# Plex to Letterboxd Export

This project exports your Plex watched movie history to a CSV file, with features such as:
- **Rewatch Tracking:** Marks movies as rewatch if they've been watched more than once.
- **User Ratings:** Captures user ratings from Plex (if available).
- **History Tracking:** Exports only new watch events (based on a stored history file).
- **Scheduling:** Runs the export immediately on startup and then daily at a specified time.

## Files in the Project

- **export_plex.py:**  
  The main, unified Python script that:
  - Reads configuration from environment variables.
  - Connects to Plex.
  - Iterates over specified libraries to collect watched movie data.
  - Exports the data to a CSV file.
  - Tracks already exported events in a JSON history file.
  - Schedules the export job to run daily.

- **Dockerfile:**  
  Builds the Docker container using a lightweight Alpine-based Python image.

- **docker-compose.yml:**  
  Defines the service, including environment variables and volume mappings.  
  *Note:* This file uses host networking.

- **requirements.txt:**  
  Lists the required Python packages (`plexapi`, `pandas`, `schedule`).

- **README.md:**  
  This file.

## Configuration

The script reads the following environment variables:

- `PLEX_URL`  
  The URL of your Plex server (e.g., `http://192.168.1.139:32400`).

- `PLEX_TOKEN`  
  Your Plex authentication token.

- `SCHEDULE_TIME`  
  The time of day to run the export job (default: `03:00`).

- `PLEX_LIBRARIES`  
  A comma-separated list of Plex library names to export (default: `Movies`).

- `EXPORT_DIR`  
  The directory where the CSV file and other output files will be saved (default: `/output`).

## Usage

1. **Local Testing:**  
   You can run the script locally if you set the required environment variables:
   ```bash
   export PLEX_URL="http://192.168.1.139:32400"
   export PLEX_TOKEN="your_plex_token"
   export SCHEDULE_TIME="03:00"
   export PLEX_LIBRARIES="Movies,Queer Film,Theatre,Concerts"
   export EXPORT_DIR="/output"
   python3 export_plex.py
