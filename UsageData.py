__author__ = 'lancejenkin'
import sqlite3
import config


def get_usage(phase, start_time, end_time):
    # Get all the usage points for the specified phases between the
    # start and end UTC timestamps.
    # Timestamps are given in seconds since epoch
    db = sqlite3.connect(config.DB_FILE)

    cursor = db.cursor()
    if start_time == end_time == 0:
        cursor.execute("SELECT utc_timestamp, energy_usage "
                       "FROM state_readings WHERE meter_box = ?", (phase,))
    elif end_time == 0:
        # Only start time set, get all records since start
        cursor.execute("SELECT utc_timestamp, energy_usage FROM state_readings "
                       "WHERE meter_box = ? AND "
                       "utc_timestamp > ?", (phase, start_time))
    else:
        cursor.execute("SELECT utc_timestamp, energy_usage FROM state_readings "
                "WHERE meter_box = ? AND "
                "utc_timestamp BETWEEN ? AND ?", (phase, start_time, end_time))

    results = cursor.fetchall()

    cursor.close()
    db.close()

    return results
