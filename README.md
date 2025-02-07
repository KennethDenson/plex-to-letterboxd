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
  The URL of your Plex server (e.g., `(http://{youripaddress}:32400).

- `PLEX_TOKEN`  
  Your Plex authentication token.

- `SCHEDULE_TIME`  
  The time of day to run the export job (default: `03:00`).

- `PLEX_LIBRARIES`  
  A comma-separated list of Plex library names to export (default: `Movies`).


## 📦 Docker Compose Example
Create a `docker-compose.yml` file with the following content:

```yaml
version: "3.8"

services:
  plex-to-letterboxd:
    image: kennethrdenson/plex-to-letterboxd:latest
    container_name: new-plex-to-letterboxd
    restart: unless-stopped
    network_mode: "host"
    environment:
      - TZ=America/Chicago
      - PLEX_URL=${PLEX_URL}
      - PLEX_TOKEN=${PLEX_TOKEN}
      - SCHEDULE_TIME=${SCHEDULE_TIME}
      - PLEX_LIBRARIES=${PLEX_LIBRARIES}
      - EXPORT_DIR=${EXPORT_DIR}
    volumes:
      - /synology/nas/plex-to-letterboxd:/output
    env_file:
      - .env
```

.env File Format

```yaml
# Plex server URL (e.g., http://192.168.1.100:32400)
PLEX_URL=http://your-plex-server:32400

# Plex API token (Find in Plex settings)
PLEX_TOKEN=your-plex-token-here

# Time to run the export job (24-hour format)
SCHEDULE_TIME=03:00

# Comma-separated list of Plex libraries to scan
PLEX_LIBRARIES=Movies,Documentaries
```


## Usage

1. **Local Testing:**  
   You can run the script locally if you set the required environment variables:
   ```bash
   export PLEX_URL="http://{youripaddress}:32400"
   export PLEX_TOKEN="your_plex_token"
   export SCHEDULE_TIME="03:00"
   export PLEX_LIBRARIES="Movies,Documentaries"
   python3 export_plex.py
