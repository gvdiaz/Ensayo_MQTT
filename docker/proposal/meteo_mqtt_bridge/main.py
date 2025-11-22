import json
import time
import logging
from typing import Dict, Any
import paho.mqtt.client as mqtt
from config import PUBLIC_BROKER_CONFIG, CEDALO_BROKERS, CHANNEL_NAMES

# mytransport = 'websockets'
mytransport = 'tcp'
myprotocol=mqtt.MQTTv5
s_keepalive = 60

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("MeteoMQTTBridge")

class MeteoMQTTBridge:
    def __init__(self):
        self.public_client = None
        self.cedalo_clients = {}
        self.received_data = {}
        
    def setup_cedalo_client(self, client_name: str, config: Dict[str, Any]) -> mqtt:
        print(config)
        try:
            client = mqtt.Client(client_id=config["client_id"],
                                transport=mytransport,
                                protocol=myprotocol)
            
            # Set credentials if provided
            if config.get("username"):
                client.username_pw_set(config["username"], config["password"])
            
            # Set callbacks
            client.on_connect = self.on_cedalo_connect
            client.on_disconnect = self.on_cedalo_disconnect
            
            # Connect
            client.connect(config["host"], config["port"], s_keepalive)
            client.loop_start()
            
            logger.info(f"Connected to Cedalo broker: {client_name} at {config['host']}:{config['port']}")
            return client
            
        except Exception as e:
            logger.error(f"Failed to connect to Cedalo broker {client_name}: {str(e)}")
            return None
    
    def on_public_message(self, client, userdata, msg):
        """Handle incoming messages from public broker"""
        try:
            topic = msg.topic
            payload = msg.payload.decode()
            
            logger.info(f"Received from public broker - Topic: {topic}, Payload: {payload}")
            
            # Store the received data
            sensor_type = topic.split('/')[-1]
            self.received_data[sensor_type] = {
                "value": payload,
                "timestamp": time.time(),
                "original_topic": topic
            }
            
            # Forward to all Cedalo brokers with custom channel names
            self.forward_to_cedalo(sensor_type, payload)
            
        except Exception as e:
            logger.error(f"Error processing public message: {str(e)}")
    
    def forward_to_cedalo(self, sensor_type: str, value: str):
        """Forward data to all Cedalo brokers with custom channel names"""
        for client_name, cedalo_client in self.cedalo_clients.items():
            if cedalo_client and cedalo_client.is_connected():
                try:
                    # Get custom channel configuration
                    channel_config = CHANNEL_NAMES.get(client_name, {})
                    base_topic = channel_config.get("base_topic", "meteo/default/")
                    channel_mapping = channel_config.get("channels", {})
                    
                    # Get custom channel name or use default
                    custom_channel = channel_mapping.get(sensor_type, sensor_type)
                    full_topic = f"{base_topic}{custom_channel}"
                    
                    # Create payload with metadata
                    payload = {
                        "value": value,
                        "sensor_type": sensor_type,
                        "custom_channel": custom_channel,
                        "timestamp": time.time(),
                        "bridge_version": "1.0"
                    }
                    
                    # Publish to Cedalo
                    cedalo_client.publish(full_topic, json.dumps(payload))
                    logger.info(f"Forwarded to {client_name} - Topic: {full_topic}, Value: {value}")
                    
                except Exception as e:
                    logger.error(f"Failed to forward to {client_name}: {str(e)}")
    
    def on_public_connect(self, client, userdata, flags, rc):
        """Callback for public broker connection"""
        if rc == 0:
            logger.info("Successfully connected to public MQTT broker")
            # Subscribe to all meteorological topics
            for topic in PUBLIC_BROKER_CONFIG["topics"]:
                client.subscribe(topic)
                logger.info(f"Subscribed to topic: {topic}")
        else:
            logger.error(f"Failed to connect to public broker, return code: {rc}")
    
    def on_cedalo_connect(self, client, userdata, flags, rc, v5config=None):
        """Callback for Cedalo broker connections"""
        if rc == 0:
            logger.info(f"Successfully connected to Cedalo broker")
        else:
            logger.error(f"Failed to connect to Cedalo broker, return code: {rc}")
    
    def on_cedalo_disconnect(self, client, userdata, rc, properties):
        """Callback for Cedalo broker disconnections"""
        logger.warning(f"Disconnected from Cedalo broker, return code: {rc}")
    
    def setup_public_client(self):
        """Setup and connect to public MQTT broker"""
        try:
            self.public_client = mqtt.Client()
            self.public_client.on_connect = self.on_public_connect
            self.public_client.on_message = self.on_public_message
            
            config = PUBLIC_BROKER_CONFIG
            self.public_client.connect(config["host"], config["port"], config["keepalive"])
            logger.info(f"Connecting to public broker: {config['host']}:{config['port']}")
            
        except Exception as e:
            logger.error(f"Failed to connect to public broker: {str(e)}")
    
    def start(self):
        """Start the MQTT bridge"""
        logger.info("Starting Meteo MQTT Bridge...")
        
        # Setup Cedalo clients
        for client_name, config in CEDALO_BROKERS.items():
            self.cedalo_clients[client_name] = self.setup_cedalo_client(client_name, config)
        
        # Setup public client
        self.setup_public_client()
        
        # Start public client loop
        if self.public_client:
            self.public_client.loop_start()
        
        logger.info("Meteo MQTT Bridge started successfully!")
    
    def stop(self):
        """Stop the MQTT bridge"""
        logger.info("Stopping Meteo MQTT Bridge...")
        
        if self.public_client:
            self.public_client.loop_stop()
            self.public_client.disconnect()
        
        for client_name, client in self.cedalo_clients.items():
            if client:
                client.loop_stop()
                client.disconnect()
                logger.info(f"Disconnected from {client_name}")
        
        logger.info("Meteo MQTT Bridge stopped")

def main():
    """Main function"""
    bridge = MeteoMQTTBridge()
    
    try:
        bridge.start()
        
        # Keep the script running
        logger.info("Press Ctrl+C to stop...")
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Received interrupt signal...")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
    finally:
        bridge.stop()

if __name__ == "__main__":
    main()