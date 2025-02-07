from plexapi.server import PlexServer
import csv
import datetime
import os
import json
import pandas as pd
import sys
import time
import schedule

# Read environment variables
PLEX_URL = os.getenv("PLEX_URL")
PLEX_TOKEN = os.getenv("PLEX_TOKEN")
SCHEDULE_TIME = os.getenv("SCHEDULE_TIME", "03:00")  # Default: Runs at 3:00 AM
LIBRARIES = os.getenv("PLEX_LIBRARIES", "Movies").split(",")
OUTPUT_DIR = os.getenv("EXPORT_DIR", "/output")

# Ensure Plex credentials are set
if not PLEX_URL or not PLEX_TOKEN:
    print("❌ Error: PLEX_URL and PLEX_TOKEN must be set.")
    sys.exit(1)

# Connect to Plex
try:
    plex = PlexServer(PLEX_URL, PLEX_TOKEN)
    print(f"✅ Connected to Plex at {PLEX_URL}")
except Exception as e:
    print(f"❌ Error connecting to Plex: {e}")
    sys.exit(1)

# Paths for CSV and logs
csv_filename = os.path.join(OUTPUT_DIR, "plex-watched-movies.csv")
history_file = os.path.join(OUTPUT_DIR, "exported_history.json")
log_file = os.path.join(OUTPUT_DIR, "export_log.txt")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def log_message(message):
    """Log messages to both console and a file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {message}"
    print(log_entry)
    sys.stdout.flush()
    with open(log_file, "a") as log:
        log.write(log_entry + "\n")

def export_watched_movies():
    """Export watched movies from Plex to CSV."""
    log_message("📢 Plex to Letterboxd export started.")
    
    # Load history
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            exported_history = set(json.load(f))
    else:
        exported_history = set()

    new_movies = []
    for library_name in LIBRARIES:
        try:
            library = plex.library.section(library_name.strip())
            movies = library.all()
            log_message(f"📁 Processing library: {library_name}")

            for movie in movies:
                if movie.viewCount > 0:
                    watched_date = movie.lastViewedAt.strftime('%Y-%m-%d') if movie.lastViewedAt else ""
                    identifier = f"{movie.title}_{watched_date}"
                    if identifier in exported_history:
                        continue
                    
                    new_movies.append({
                        "Title": movie.title,
                        "Year": movie.year,
                        "WatchedDate": watched_date,
                        "Rewatch": "Yes" if movie.viewCount > 1 else "No"
                    })
                    
                    exported_history.add(identifier)
                    log_message(f"➕ Added: {movie.title} ({movie.year}) - Watched on {watched_date}")

        except Exception as e:
            log_message(f"❌ Error processing library '{library_name}': {e}")

    # Save updated history
    with open(history_file, "w") as f:
        json.dump(list(exported_history), f)

    # Save to CSV
    if new_movies:
        pd.DataFrame(new_movies).to_csv(csv_filename, mode="a", header=not os.path.exists(csv_filename), index=False)
        log_message(f"✅ {len(new_movies)} new movies added to CSV.")
    else:
        log_message("✅ No new movies to export.")

# Schedule the export
schedule.every().day.at(SCHEDULE_TIME).do(export_watched_movies)

# Run the script immediately on startup
export_watched_movies()

# Keep running the scheduler in a loop
while True:
    schedule.run_pending()
    
    # Fetch the next scheduled job time and log it
    next_run = schedule.next_run()
    if next_run:
        log_message(f"⏳ Scheduler is active. Next run at {next_run.strftime('%H:%M')} daily...")

    time.sleep(60)  # Check every minute
