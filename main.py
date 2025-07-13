from drowsiness_detector import eye_start_monitoring
from alarm import play_alarm
from location_alert import get_location, send_alert


def main():
    eye_start_monitoring()
    play_alarm()
    send_alert()