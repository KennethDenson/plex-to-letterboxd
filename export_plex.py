from plexapi.server import PlexServer
import csv
import datetime
import re
import os
import json
import pandas as pd
import sys
import time
import subprocess
from croniter import croniter
import pytz

# Read Plex credentials from environment variables
PLEX_URL = os.getenv("PLEX_URL")
PLEX_TOKEN = os.getenv("PLEX_TOKEN")
CRON_SCHEDULE = os.getenv("CRON_SCHEDULE", "0 3 * * *")  # Default: Runs every day at 3 AM
SYSTEM_TIMEZONE = os.getenv("TZ", "UTC")  # Read system timezone from env, default to UTC

# Ensure Plex credentials are set
if not PLEX_URL or not PLEX_TOKEN:
    print("❌ Error: PLEX_URL and PLEX_TOKEN must be set as environment variables.")
    sys.exit(1)

# Get library names from the environment variable (default to "Movies")
LIBRARIES = os.getenv("PLEX_LIBRARIES", "Movies").split(",")

# Connect to Plex
try:
    plex = PlexServer(PLEX_URL, PLEX_TOKEN)
    print(f"✅ Connected to Plex at {PLEX_URL}")
except Exception as e:
    print(f"❌ Error connecting to Plex: {e}")
    sys.exit(1)

# Function to extract TMDb ID from Plex GUID
def extract_tmdb_id(guid):
    match = re.search(r'tmdb://(\d+)', guid)
    return match.group(1) if match else ""

# Path to files
output_dir = os.getenv("EXPORT_DIR", "/output") 
csv_filename = os.path.join(output_dir, "plex-watched-movies.csv")
history_file = os.path.join(output_dir, "exported_history.json")
log_file = os.path.join(output_dir, "export_log.txt")

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Function to log messages to both file and console
def log_message(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {message}"
    print(log_entry)
    sys.stdout.flush()
    with open(log_file, "a") as log:
        log.write(log_entry + "\n")

log_message("📢 Plex to Letterboxd export started.")

# Load watched history
if os.path.exists(history_file):
    with open(history_file, "r") as f:
        exported_history = set(json.load(f))
else:
    exported_history = set()

watched_movies = []
new_movies = []

for library_name in LIBRARIES:
    library_name = library_name.strip()
    try:
        library = plex.library.section(library_name)
        movies = library.all()
        log_message(f"📁 Processing library: {library_name}")

        for movie in movies:
            if movie.viewCount > 0:
                watched_date = movie.lastViewedAt.strftime('%Y-%m-%d') if movie.lastViewedAt else ""
                identifier = f"{movie.title}_{watched_date}"
                if identifier in exported_history:
                    continue
                
                tmdb_id = extract_tmdb_id(movie.guid)
                genres = ", ".join([g.tag for g in movie.genres]) if movie.genres else ""
                studio = movie.studio if movie.studio else ""
                directors = ", ".join([d.tag for d in movie.directors]) if movie.directors else ""
                rewatch = "Yes" if movie.viewCount > 1 else "No"
                
                new_movies.append({
                    "Title": movie.title,
                    "Year": movie.year,
                    "WatchedDate": watched_date,
                    "LetterboxdURI": "",
                    "Rating": movie.userRating if movie.userRating else "",
                    "Review": "",
                    "Tags": "",
                    "Rewatch": rewatch,
                    "Director(s)": directors,
                    "Studio": studio,
                    "Genres": genres,
                    "TMDb ID": tmdb_id
                })
                
                exported_history.add(identifier)
                log_message(f"➕ Added: {movie.title} ({movie.year}) - Watched on {watched_date}")

    except Exception as e:
        log_message(f"❌ Error processing library '{library_name}': {e}")

# Save updated history
with open(history_file, "w") as f:
    json.dump(list(exported_history), f)

# Append new movies to CSV
if new_movies:
    new_df = pd.DataFrame(new_movies)
    new_df.to_csv(csv_filename, mode="a", header=not os.path.exists(csv_filename), index=False, encoding="utf-8")
    log_message(f"✅ {len(new_movies)} new movies added to CSV.")
else:
    log_message("✅ No new movies to export.")

# Calculate the next scheduled cron run time
def get_next_run_time(cron_schedule, system_timezone):
    try:
        local_tz = pytz.timezone(system_timezone)
        now_local = datetime.datetime.now(local_tz)
        
        # Calculate next run time in local timezone
        cron = croniter(cron_schedule, now_local)
        next_run_local = cron.get_next(datetime.datetime)
        
        # Convert to local timezone explicitly
        next_run_dt = local_tz.localize(next_run_local) if next_run_local.tzinfo is None else next_run_local
        
        return next_run_dt.strftime("%Y-%m-%d %H:%M:%S %Z")
    except Exception as e:
        return f"⚠️ Error calculating next cron run: {e}"

try:
    next_run = get_next_run_time(CRON_SCHEDULE, SYSTEM_TIMEZONE)
    log_message(f"⏳ Next scheduled run: {next_run}")
except Exception as e:
    log_message(f"⚠️ Unable to determine next cron run time: {e}")

log_message("📢 Export process complete.\n")
