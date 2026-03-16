import json
import uuid
from confluent_kafka import Producer
from logger.logger import log_event


class KafkaProducer:
    def __init__(self, bootstrap_servers: str, topic: str):
        self.topic = topic
        producer_config = {
            "bootstrap.servers": bootstrap_servers
        }
        self.producer = Producer(producer_config)
        
    def delivery_report(self, err, msg):
        if err:
            print(f"❌ Delivery failed: {err}")
        else:
            print(f"✅ Delivered {msg.value().decode("utf-8")}")
            print(f"✅ Delivered to {msg.topic()} : partition {msg.partition()} : at offset {msg.offset()}")
    
    def send(self, msg):
        value = json.dumps(msg).encode("utf-8")
        self.producer.produce(
            topic= self.topic,
            value=value,
            callback=self.delivery_report
        )
    
    def flush(self):
        self.producer.flush()