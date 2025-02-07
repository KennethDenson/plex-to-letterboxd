# Plex to Letterboxd Exporter

This container connects to your **Plex** server, extracts your **watched movies**, and prepares them for easy import into **Letterboxd**. It doesn't appear that Letterboxd has an API for adding directly to your watched films, so this import option is the best we have for now.

## Features
- **Automated Export**: Fetches watched movies from Plex at a scheduled time.
- **CSV Generation**: Outputs a `.csv` file compatible with **Letterboxd import**.
- **Multi-Platform Support**: Runs on **x86 (AMD64) and ARM (Raspberry Pi, M1/M2 Mac)**.
- **Persistent History**: Keeps track of already exported movies to avoid duplicates.
- **Lightweight & Efficient**: Runs as a simple **Docker container**.

---

## Installation

### 1️⃣ Pull the Docker Image
```sh
docker pull kennethrdenson/plex-to-letterboxd:latest
```

### 2️⃣ Create a `docker-compose.yml` File
Save the following as `docker-compose.yml`:

```yaml
version: '3.8'

services:
  plex-to-letterboxd:
    image: kennethrdenson/plex-to-letterboxd:latest
    container_name: plex-to-letterboxd
    restart: unless-stopped

    environment:
      # Set your Plex server URL (Example: http://192.168.1.xxx:32400)
      - PLEX_URL=http://your-plex-server-ip:32400

      # Your Plex API token (Retrieve from Plex web app → Network settings)
      - PLEX_TOKEN=your_plex_token_here

      # List of Plex libraries to scan (Separate multiple libraries with commas)
      - PLEX_LIBRARIES=Movies,Documentaries

      # Set export schedule time (Format: HH:MM) - Example: 03:00 for 3:00 AM daily
      - SCHEDULE_TIME=03:00

    volumes:
      # Map an output directory on your host machine to store exported CSV files
      - /absolute/path/on/your/machine:/output
```

### 3️⃣ Start the Container
```sh
docker compose up -d
```

### 4️⃣ Check Logs
To verify it's running correctly:
```sh
docker logs -f plex-to-letterboxd
```

---

## Output & Letterboxd Import

The watched movies list is **saved as CSV** in `./output/plex-watched-movies.csv`.

### How to Import into Letterboxd
1. Go to [Letterboxd Import Page](https://letterboxd.com/import/)
2. Upload `plex-watched-movies.csv`
3. Confirm your import!
4. **Delete the CSV file after import** to prevent re-importing the same movies in future runs.

### Files Created in the Output Directory
- `plex-watched-movies.csv`: The export file for Letterboxd import.
- `exported_history.json`: Tracks which movies have already been exported to prevent duplicates.

**Important:** Do not delete `exported_history.json` unless you want to reset your export history and re-import all watched movies.

---

## Environment Variables

| Variable         | Default | Description |
|-----------------|---------|-------------|
| `PLEX_URL` | **(Required)** | Your Plex server URL (e.g., `http://192.168.1.139:32400`) |
| `PLEX_TOKEN` | **(Required)** | Your Plex authentication token (get it from Plex API) |
| `PLEX_LIBRARIES` | `Movies` | Comma-separated list of Plex libraries to scan |
| `SCHEDULE_TIME` | `03:00` | Time (HH:MM) for daily export |

---

## Updating the Container

To **update to the latest version**, run:
```sh
docker compose pull
docker compose up -d --force-recreate
```

---

## Changelog
- **1.0.1** - Stable release with improved scheduling and logging.

---

## AI Acknowledgement
Some aspects of this project, including code optimizations and documentation, were assisted by AI suggestions. However, all final decisions, modifications, and implementations were done manually.

---

## License
MIT License - Feel free to use and modify!

