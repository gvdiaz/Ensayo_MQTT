import os
from dotenv import load_dotenv

load_dotenv()

# Public MQTT Broker Configuration (Source)
PUBLIC_BROKER_CONFIG = {
    "host": "broker.hivemq.com",  # Public test broker
    "port": 1883,
    "keepalive": 60,
    "topics": [
        "meteo/temperature",
        "meteo/humidity", 
        "meteo/pressure",
        "meteo/wind",
        "meteo/rainfall"
    ]
}

# Cedalo Platform Configuration (Destination)
CEDALO_BROKERS = {
    "client_1": {
        "host": os.getenv("CEDALO_1_HOST", "your-cedalo-instance-1.cedalo.com"),
        "port": int(os.getenv("CEDALO_1_PORT", "1883")),
        "username": os.getenv("CEDALO_1_USERNAME", ""),
        "password": os.getenv("CEDALO_1_PASSWORD", ""),
        "client_id": "meteo_bridge_1"
    },
    "client_2": {
        "host": os.getenv("CEDALO_2_HOST", "your-cedalo-instance-2.cedalo.com"),
        "port": int(os.getenv("CEDALO_2_PORT", "1883")),
        "username": os.getenv("CEDALO_2_USERNAME", ""),
        "password": os.getenv("CEDALO_2_PASSWORD", ""),
        "client_id": "meteo_bridge_2"
    },
    "client_3": {
        "host": os.getenv("CEDALO_3_HOST", "your-cedalo-instance-3.cedalo.com"),
        "port": int(os.getenv("CEDALO_3_PORT", "1883")),
        "username": os.getenv("CEDALO_3_USERNAME", ""),
        "password": os.getenv("CEDALO_3_PASSWORD", ""),
        "client_id": "meteo_bridge_3"
    }
}

# Channel naming configuration
CHANNEL_NAMES = {
    "client_1": {
        "base_topic": "weather_station/central/",
        "channels": {
            "temperature": "ambient_temperature",
            "humidity": "relative_humidity", 
            "pressure": "atmospheric_pressure",
            "wind": "wind_speed",
            "rainfall": "precipitation"
        }
    },
    "client_2": {
        "base_topic": "environmental_sensors/city/",
        "channels": {
            "temperature": "temp_celsius",
            "humidity": "humidity_percent",
            "pressure": "pressure_hpa",
            "wind": "wind_velocity",
            "rainfall": "rain_mm"
        }
    },
    "client_3": {
        "base_topic": "iot_meteo/aggregated/",
        "channels": {
            "temperature": "thermal_reading",
            "humidity": "moisture_level",
            "pressure": "barometric_data", 
            "wind": "air_flow",
            "rainfall": "hydrometer"
        }
    }
}