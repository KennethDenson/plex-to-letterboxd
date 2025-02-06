#!/bin/sh

# Set default cron schedule if not provided
CRON_SCHEDULE=${CRON_SCHEDULE:-"0 3 * * *"}  # Default: Runs every day at 3 AM

echo "Setting up timezone..."
ln -sf /usr/share/zoneinfo/$TZ /etc/localtime
echo "$TZ" > /etc/timezone

echo "Setting up cron job: $CRON_SCHEDULE"

# Ensure no leftover cron PID file
rm -f /var/run/crond.pid

# Write the cron job to a file
echo "$CRON_SCHEDULE python3 /app/export_plex.py >> /proc/1/fd/1 2>&1" > /etc/cron.d/plex-cron

# Ensure correct permissions and load the new cron job
chmod 0644 /etc/cron.d/plex-cron
crontab /etc/cron.d/plex-cron

# Run the script immediately once
echo "Running export_plex.py immediately..."
python3 /app/export_plex.py

# Start cron in the foreground to prevent crashes
exec cron -f
