import requests
import time
from bs4 import BeautifulSoup

# Webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1354643640043176047/UZKq65DtrZrt0P5sP_YeT9_5r-MDpaZAQCWpdyA8hweU7P2fcLR7w3AT_OYeKNUNtwg8"

# Target products to monitor
PRODUCTS_TO_WATCH = ["Crusader", "Lethal Lite", "Lethal Full"]

# Store previous status
previous_status = {}

def fetch_status():
    """Scrapes the website and gets the product statuses."""
    response = requests.get("https://visuals.gg/status")
    if response.status_code != 200:
        print("Failed to fetch the website.")
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    statuses = {}
    for product in PRODUCTS_TO_WATCH:
        product_element = soup.find(text=product)
        if product_element:
            status_element = product_element.find_next("span")  # Adjust this if needed
            if status_element:
                statuses[product] = status_element.text.strip()
    
    return statuses

def send_webhook_message(product, status):
    """Sends a status update to Discord."""
    status_messages = {
        "Updated": f"{product} is Now **Updated**",
        "Updating": f"{product} is Updating..",
        "Undetected": f"{product} is Undetected"
    }
    
    message = status_messages.get(status, f"{product} status changed to {status}")
    
    data = {"content": message}
    response = requests.post(WEBHOOK_URL, json=data)
    
    if response.status_code == 204:
        print(f"Sent update: {message}")
    else:
        print("Failed to send webhook.")

def monitor():
    """Continuously checks for status updates."""
    global previous_status

    while True:
        current_status = fetch_status()
        
        if current_status:
            for product, status in current_status.items():
                if previous_status.get(product) != status:
                    send_webhook_message(product, status)
                    previous_status[product] = status

        time.sleep(60)  # Check every 60 seconds

if __name__ == "__main__":
    monitor()
