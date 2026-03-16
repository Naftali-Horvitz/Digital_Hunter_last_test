from consumer import KafkaConsumer
from mongo_client import Mongo
from modules import Intelligence
from logger.logger import log_event
from kafka_producer import KafkaProducer
import config
from orchestrator import Orchestrator


def main():
    bootstrap_servers = config.bootstrap_servers
    mongo_uri = config.mongo_uri
    topic = config.topic
    err_topic = config.err_topic
    db_name = config.db_name
    col_name = config.col_name
    consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers, topic=topic)
    mongo = Mongo(mongo_uri=mongo_uri, db_name=db_name, col_name=col_name)
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers, topic=err_topic)
    orchestrator = Orchestrator(consumer=consumer, mongo=mongo, producer=producer)
    orchestrator.run()
    
if __name__ =="__main__":
    main()