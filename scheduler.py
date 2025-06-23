import time
from main import main as run_sync

def run_scheduler(interval_seconds=300):
    while True:
        try:
            print("Running scheduled sync...")
            run_sync()
        except Exception as e:
            print("Scheduled sync failed:", e)
        time.sleep(interval_seconds)

if __name__ == "__main__":
    run_scheduler()
