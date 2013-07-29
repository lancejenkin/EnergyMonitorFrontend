__author__ = 'lancejenkin'
import pymysql
import config

MYSQL_HOST = "localhost"
MYSQL_USER = "lance"
MYSQL_PASS = "lance"
MYSQL_DB = "energy_monitor"

def get_usage(phase, start_time, end_time):
    # Get all the usage points for the specified phases between the
    # start and end UTC timestamps.
    # Timestamps are given in seconds since epoch
    db = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS, MYSQL_DB)

    cursor = db.cursor()
    if start_time == end_time == 0:
        cursor.execute("SELECT `utc_timestamp`, `energy_usage` "
                       "FROM collated_readings WHERE `meter_box` = %s", (phase,))
    elif end_time == 0:
        # Only start time set, get all records since start
        cursor.execute("SELECT `utc_timestamp`, `energy_usage` FROM `collated_readings` "
                       "WHERE `meter_box` = %s AND "
                       "`utc_timestamp` > %s", (phase, start_time))
    else:
        cursor.execute("SELECT `utc_timestamp`, `energy_usage` FROM `collated_readings` "
                "WHERE `meter_box` = %s AND "
                "`utc_timestamp` BETWEEN %s AND %s", (phase, start_time, end_time))

    results = cursor.fetchall()

    cursor.close()
    db.close()

    return results
