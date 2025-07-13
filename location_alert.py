#Location alert
from geopy.geocoders import Nominatim 
import requests


def get_location():
    try:
        response = requests.get("https://ipinfo.io/json/")
        data = response.json()
        loc = data['loc']
        return loc
    except Exception as e:
        print(f"Error: {e}")
        return None
        
def send_alert(username, token):
    loc = get_location()
    if loc:
        message = f"Drowsiness detected! Driver's last known location: {loc}"
    else:
        message = "Drowsiness detected! Unable to retrieve location."
    url = f"https://api.callmebot.com/telegram/send.php?user=@{username}&text={requests.utils.quote(message)}&token={token}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("✅ Alert sent via Telegram!")
        else:
            print(f"❌ Failed to send alert. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"❌ Exception while sending alert: {e}")

get_location()