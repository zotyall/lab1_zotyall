#!/bin/bash

# organizer.sh
# Archives grades.csv with a timestamp, resets workspace, and logs the operation.

GRADES_FILE="grades.csv"
ARCHIVE_DIR="archive"
LOG_FILE="organizer.log"

# 1. Check if grades.csv exists before doing anything
if [ ! -f "$GRADES_FILE" ]; then
    echo "Error: '$GRADES_FILE' not found in the current directory. Nothing to archive."
    exit 1
fi

# 2. Create the archive directory if it doesn't exist
if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir -p "$ARCHIVE_DIR"
    echo "Created directory: $ARCHIVE_DIR"
fi

# 3. Generate a timestamp (format: YYYYMMDD-HHMMSS)
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

# 4. Build the new archived filename
ARCHIVED_NAME="grades_${TIMESTAMP}.csv"
ARCHIVED_PATH="${ARCHIVE_DIR}/${ARCHIVED_NAME}"

# 5. Move and rename grades.csv into the archive directory
mv "$GRADES_FILE" "$ARCHIVED_PATH"
echo "Archived: '$GRADES_FILE' → '$ARCHIVED_PATH'"

# 6. Create a fresh empty grades.csv in the current directory
touch "$GRADES_FILE"
echo "Reset: New empty '$GRADES_FILE' created."

# 7. Log the operation (append to organizer.log)
LOG_ENTRY="[${TIMESTAMP}] Original: ${GRADES_FILE} | Archived as: ${ARCHIVED_PATH}"
echo "$LOG_ENTRY" >> "$LOG_FILE"
echo "Logged to: $LOG_FILE"

echo "Done."
