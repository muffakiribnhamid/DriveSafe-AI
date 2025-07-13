#Location alert
from geopy.geocoders import Nominatim 
import requests


def get_location():
    try:
        response = requests.get("http://ip-api.com/json/", timeout=3)
        data = response.json()
        if data.get('status') == 'success':
            lat = data.get('lat')
            lon = data.get('lon')
            if lat is not None and lon is not None:
                return f"{lat},{lon}"
    except Exception as e:
        print(f"ip-api.com error: {e}")
    try:
        response = requests.get("https://geolocation-db.com/json/", timeout=3)
        data = response.json()
        lat = data.get('latitude')
        lon = data.get('longitude')
        if lat is not None and lon is not None:
            return f"{lat},{lon}"
    except Exception as e:
        print(f"geolocation-db.com error: {e}")
    return None

def send_alert(username):
    """
    Send a Telegram alert via CallMeBot, including location if available.
    Args:
        username (str): Telegram username (without @)
    """
    loc = get_location()
    if loc:
        message = f"Hey your driver is sort of drowsy! Please contact him ASAP. Location: {loc}"
    else:
        message = "Hey your driver is sort of drowsy! Please contact him ASAP. Location unavailable."
    url = f"https://api.callmebot.com/text.php?user={username}&text={requests.utils.quote(message)}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("✅ Alert sent via Telegram!")
        else:
            print(f"❌ Failed to send alert. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"❌ Exception while sending alert: {e}")

