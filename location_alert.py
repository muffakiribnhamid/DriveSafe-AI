#Location alert
from geopy.geocoders import Nominatim 
import requests


        
def send_alert(username):
    """
    Send a Telegram alert via CallMeBot.
    Args:
        username (str): Telegram username (without @)
    """
    message = "Hey your driver is sort of drowsy! Please contact him ASAP"
    url = f"https://api.callmebot.com/text.php?user={username}&text={requests.utils.quote(message)}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("✅ Alert sent via Telegram!")
        else:
            print(f"❌ Failed to send alert. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"❌ Exception while sending alert: {e}")

