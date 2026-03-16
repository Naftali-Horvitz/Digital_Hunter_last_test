from confluent_kafka import Consumer, KafkaException
from logger.logger import log_event
from typing import Callable
import json

class consumer_kafka:
    def __init__(self, bootstrap_servers: str, topic: str):
        config = {
            "bootstrap.servers" : bootstrap_servers,
            "group.id": "intel-1",
            "auto.offset.reset": "earliest"
        }
        try:
            self.consumer = Consumer(config)
            self.consumer.subscribe([topic])
            print("🟢 Consumer is running and subscribed to orders topic")
            log_event(level="info", message=f"Consumer is running and subscribed to {topic} topic")
        except KafkaException as e:
            print("Consumer failed running")
            log_event(level="error", message=f"Consumer failed running: {e}")
    
    def start(self, callable: Callable):
        try:
            while True:
                msg = self.consumer.poll()
                if msg is None:
                    continue
                if msg.error():
                    log_event(level="error", message=f"msg error: {msg.error()}")
                    print("❌ Error:", msg.error())
                    continue
                value = msg.value().decode("utf-8")
                intelligence_data = json.loads(value)
                print(f"intelligence data: {intelligence_data}")
                callable(intelligence_data)
        except Exception as e:
            print(f"\n🔴 Stopping consumer: {e}")
        finally:
            self.consumer.close()
                    