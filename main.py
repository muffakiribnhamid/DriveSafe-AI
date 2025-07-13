"""
Main entry point for Driver-AI Drowsiness Detection System.

Set your Telegram username and CallMeBot token below.
"""
from drowsiness_detector import detect_drowsiness

# === CONFIGURATION ===
TELEGRAM_USERNAME = "Bhattzaid"  # Without @


def main():
    detect_drowsiness(TELEGRAM_USERNAME)

if __name__ == "__main__":
    main()