from confluent_kafka import Consumer, KafkaException
from logger.logger import log_event
from typing import Callable
import json
from rich import print as rprint
class KafkaConsumer:
    def __init__(self, bootstrap_servers: str, topic: str):
        config = {
            "bootstrap.servers" : bootstrap_servers,
            "group.id": "intel-1",
            "auto.offset.reset": "earliest"
        }
        try:
            self.consumer = Consumer(config)
            self.consumer.subscribe([topic])
            log_event(level="info", message=f"🟢 Consumer is running and subscribed to {topic} topic")
        except KafkaException as e:
            log_event(level="error", message=f"Consumer failed running: {e}")
    
    def start(self, callable: Callable):
        try:
            while True:
                msg = self.consumer.poll()
                if msg is None:
                    continue
                if msg.error():
                    log_event(level="error", message=f"❌ msg error: {msg.error()}")
                    continue
                try:
                    value = msg.value().decode("utf-8")
                    intelligence_data = json.loads(value)
                    log_event(level="debug", message=f"intelligence data: {intelligence_data}")
                    callable(intelligence_data)
                except Exception as e:
                    log_event(level="error", message=f"{e}")
        except Exception as e:
            log_event(level="error", message=f"🔴 Stopping consumer: {e}")
            
        finally:
            self.consumer.close()
            
            
            
if __name__ =="__main__":
    c = KafkaConsumer("localhost:9092", "intel")
    c.start()