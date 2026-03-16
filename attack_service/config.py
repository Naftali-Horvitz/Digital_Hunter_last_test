import os

bootstrap_servers = os.getenv("BOOTSTRAP_SERVERS", "localhost:9092")
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
topic = os.getenv("TOPIC", "intel")
err_topic = os.getenv("ERR_TOPIC", "intel_signals_dlq")
db_name = os.getenv("DB_NAME", "test")
col_name = os.getenv("COL_NAME", "bank_goals")