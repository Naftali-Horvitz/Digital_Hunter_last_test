from consumer import KafkaConsumer
from mongo_client import Mongo
from modules import Intelligence
from logger.logger import log_event
from haversine import haversine_km
from kafka_producer import KafkaProducer

class Orchestrator:
    def __init__(self, consumer: KafkaConsumer, mongo: Mongo, producer: KafkaProducer):
        self.consumer = consumer
        self.mongo = mongo
        self.producer = producer
    
    def validate(self, data: dict):
        try:
            data = Intelligence(**data)
            return True
        except Exception as e:
            self.producer.send(e)
            log_event(level="error", message=e)
            return False

    def extracted_from_handle_event(self, doc, get_doc, entity_id):
            new_lat = doc.get("reported_lat")
            new_lon = doc.get("reported_lon")
            prev_lat = get_doc.get("reported_lat")
            prev_lon = get_doc.get("reported_lon")
            distance = haversine_km(new_lat, new_lon, prev_lat, prev_lon)
            self.mongo.update_doc(new_lat, new_lon, distance, entity_id)
    
    def handle_event(self, doc: dict):
        if not self.validate(doc):
            return
        entity_id = doc.get("entity_id")
        get_doc = self.mongo.find_is_exists(entity_id)
        if get_doc is None:
            doc["distance"] = 0
            self.mongo.insert_doc(doc)
            log_event(level="info", message=f"insert this purpose: {entity_id}")
        else:
            if not get_doc.get("result") or get_doc.get("result") != "completed":
                self.extracted_from_handle_event(doc, get_doc, entity_id)
                log_event(level="info", message=f"update this purpose: {entity_id}")
            else:
                log_event(level="error", message=f"The this {entity_id} target has already been attacked.")
                return        

    def run(self):
        self.consumer.start(self.handle_event)