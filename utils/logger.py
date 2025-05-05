import csv
import os
from datetime import datetime

def save_session_log(username, exercise_type, reps, incorrects, accuracy):
    """
    Save the session log to a CSV file.
    """
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    log_path = os.path.join("logs", "session_logs.csv")

    file_exists = os.path.isfile(log_path)

    with open(log_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "User", "Exercise", "Reps/Time", "Incorrects", "Accuracy (%)"])

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, username, exercise_type, reps, incorrects, round(accuracy, 2)])
