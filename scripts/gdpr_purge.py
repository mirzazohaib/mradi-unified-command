import os
import datetime

LOG_FILE = "audit.log"
RETENTION_DAYS = 30

def purge_old_records():
    if not os.path.exists(LOG_FILE):
        print("No audit log found.")
        return

    print(f"Starting GDPR Compliance Purge (Retention: {RETENTION_DAYS} days)...")
    
    # Calculate cutoff date
    cutoff_date = datetime.datetime.now() - datetime.timedelta(days=RETENTION_DAYS)
    
    new_lines = []
    deleted_count = 0
    
    with open(LOG_FILE, "r") as f:
        for line in f:
            # Extract timestamp (Assuming format: 2026-01-11 10:00:00 | ...)
            try:
                timestamp_str = line.split("|")[0].strip()
                log_date = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                
                if log_date > cutoff_date:
                    new_lines.append(line)
                else:
                    deleted_count += 1
            except Exception:
                # If line is malformed, keep it to be safe
                new_lines.append(line)

    # Rewrite file
    with open(LOG_FILE, "w") as f:
        f.writelines(new_lines)

    print(f"GDPR Purge Complete. Removed {deleted_count} records older than {cutoff_date.date()}.")

if __name__ == "__main__":
    purge_old_records()