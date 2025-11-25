import json
import logging
import requests
import paho.mqtt.client as mqtt
from config import PUBLIC_BROKER_CONFIG, CEDALO_BROKERS, CHANNEL_NAMES
import time


# --------------------------
# Logging configuration
# --------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("weather_publisher")

# --------------------------
# Settings
# --------------------------
LAT = -34.61   # Buenos Aires example
LON = -58.38
BROKER = "pf-dc7qm9medgtvammb29vo.cedalo.cloud"
PORT = 1883
TOPIC = "weather/data"


# --------------------------
# MQTT Callbacks
# --------------------------
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        logger.info("Connected to MQTT broker successfully.")
    else:
        logger.error(f"Failed to connect. Reason code: {reason_code}")


def on_disconnect(client, userdata, reason_code, properties):
    logger.warning(f"Disconnected from MQTT broker. Reason code: {reason_code}")


# --------------------------
# Weather fetch function
# --------------------------
def get_weather():
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={LAT}&longitude={LON}&current_weather=true"
    )

    logger.info("Fetching weather data...")
    resp = requests.get(url)

    if resp.status_code != 200:
        logger.error(f"HTTP error: {resp.status_code}")
        return None

    data = resp.json()
    logger.info(f"Weather data retrieved: {data['current_weather']}")
    return data["current_weather"]


# --------------------------
# MQTT Setup
# --------------------------
config = CEDALO_BROKERS
print('Visualización de CEDALO_BROKERS:', config)
# visualización de variables necesarias para configuración de conexión
print('Id: ', config['client_1']['client_id'])
print('Username: ', config['client_1']['username'])
print('Pass: ', config['client_1']['password'])
client = mqtt.Client(client_id=config['client_1']['client_id'], protocol=mqtt.MQTTv5)
if config['client_1'].get("username"):
    client.username_pw_set(config['client_1']["username"], config['client_1']["password"])
client.on_connect = on_connect
client.on_disconnect = on_disconnect

logger.info(f"Connecting to broker {BROKER}:{PORT} ...")
client.connect(BROKER, PORT)
client.loop_start()


# # --------------------------
# # Publish once
# # --------------------------
# weather = get_weather()

# if weather:
#     payload = json.dumps(weather)
#     result = client.publish(TOPIC, payload, qos=1)

#     if result.rc == mqtt.MQTT_ERR_SUCCESS:
#         logger.info(f"Published weather data to topic '{TOPIC}': {payload}")
#     else:
#         logger.error(f"Failed to publish. Error code: {result.rc}")

# logger.info("Program finished.")

# --------------------------
# Publish every 30 seconds
# --------------------------
logger.info("Starting periodic weather publishing (every 30 seconds)...")

try:
    while True:
        weather = get_weather()

        if weather:
            payload = json.dumps(weather)
            result = client.publish(TOPIC, payload, qos=1)

            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logger.info(f"Published weather data to topic '{TOPIC}': {payload}")
            else:
                logger.error(f"Failed to publish. Error code: {result.rc}")
        else:
            logger.error("No weather data to publish.")

        time.sleep(30)

except KeyboardInterrupt:
    logger.info("Stopping weather publisher...")

finally:
    client.loop_stop()
    client.disconnect()
