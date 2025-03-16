import pyautogui
import cv2
import numpy as np
import requests
import time

# Settings for the Telegram bot
BOT_TOKEN = "paste your bot id here"
CHAT_ID = "paste your id here"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print(f"Error sending message: {response.text}")

def find_button_by_image(template_path, threshold=0.65):
    screenshot = pyautogui.screenshot()
    image = np.array(screenshot)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template is None:
        raise ValueError(f"Template not found at path {template_path}")

    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    print(f"Max confidence: {max_val}")  # max confidence value

    if max_val >= threshold:
        return True, max_val
    return False, max_val

if __name__ == "__main__":
    TEMPLATE_PATH = "your path to image"  # path to png image
    while True:
        found, confidence = find_button_by_image(TEMPLATE_PATH)
        if found:
            send_telegram_message(f"go accept your match! (confidence: {confidence:.2f})")
            time.sleep(0.5)  # faster spam interval
        elif confidence >= 0.65:  # check for lower confidence
            send_telegram_message(f"i think your match is ready! confidence: {confidence:.2f}")
            time.sleep(0.5)  # more frequent spam when match is likely
        time.sleep(1)  # overall loop check time (dont change it, it will slow your system)
