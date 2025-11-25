import json
import requests
import paho.mqtt.client as mqtt
from config import PUBLIC_BROKER_CONFIG, CEDALO_BROKERS, CHANNEL_NAMES

LAT = -34.61   # example: Buenos Aires
LON = -58.38

client = mqtt.Client(client_id="weather_pub", protocol=mqtt.MQTTv5)
client.connect("pf-dc7qm9medgtvammb29vo.cedalo.cloud", 1883)
if config.get("username"):
    client.username_pw_set(config["username"], config["password"])
client.loop_start()

def get_weather():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current_weather=true"
    resp = requests.get(url).json()
    return resp["current_weather"]

current = get_weather()
print(json.dumps(current))
client.publish("weather/data", json.dumps(current), qos=1)

print("Published current weather:", current)
