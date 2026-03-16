from consumer import KafkaConsumer
from mongo_client import Mongo
from modules import Intelligence
from logger.logger import log_event
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
        attack_id = doc.get("attack_id")
        timestamp_damage = doc.get("timestamp")
        weapon_type = doc.get("weapon_type")
        self.mongo.update_doc(
            attack_id=attack_id,
            timestamp_damage=timestamp_damage,
            weapon_type=weapon_type,
        )

    def handle_event(self, doc: dict):
        if not self.validate(doc):
            return
        entity_id = doc.get("entity_id")
        get_doc = self.mongo.find_is_exists(entity_id)
        
        if get_doc is None:
            self.mongo.insert_doc(doc)
            log_event(level="info", message=f"insert this purpose: {entity_id}")
        else:
            self.extracted_from_handle_event(doc, get_doc, entity_id)
            log_event(level="info", message=f"update this purpose: {entity_id}")

    def run(self):
        self.consumer.start(self.handle_event)
