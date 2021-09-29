from flask import Flask, jsonify
from flask_cors import CORS
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

@app.before_request
def before_request():
    # Set up a Kafka producer
    TOPIC_NAME = 'location_api'
    KAFKA_SERVER = 'my-release-kafka-0.my-release-kafka-headless.default.svc.cluster.local:9092'
    producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
    message=dict({'Name':'Rohan Purekar', 'status':'Alright!'})
    producer.send(TOPIC_NAME, bytes(str(message), 'utf-8'))
    producer.flush()
    # Setting Kafka to g enables us to use this
    # in other parts of our application
    g.kafka_producer = producer

def create_app(env=None):
    from app.config import config_by_name
    from app.routes import register_routes

    app = Flask(__name__)
    app.config.from_object(config_by_name[env or "test"])
    api = Api(app, title="UdaConnect Locations API", version="0.1.0")

    CORS(app)  # Set CORS for development

    register_routes(api, app)
    db.init_app(app)

    @app.route("/health")
    def health():
        return jsonify("healthy")

    return app