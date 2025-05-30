#!/bin/python3

from flask import Flask, request, jsonify
import redis
import pika
import threading

app = Flask(__name__)
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

events = {}

@app.route("/events", methods=["POST"])
def add_event():
    data = request.json
    event_id = data["id"]
    description = data["description"]

    events[event_id] = description
    redis_client.set('evento-' + str(event_id), description)

    return jsonify({"message": "Evento adicionado!", "event": {"id": event_id, "description": description}}), 201

@app.route("/events", methods=["GET"])
def get_events():
    cached_events = {key: redis_client.get(key) for key in redis_client.keys("evento-*")}
    
    return jsonify({"events": cached_events if cached_events else events})

QUEUE = 'dispatch-messages'

def receive_dispatch_alert(ch, method, properties, body):
    print(f"Mensagem recebida do logistic-service: {body.decode()}")

def consume():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE)
    channel.basic_consume(queue=QUEUE, on_message_callback=receive_dispatch_alert, auto_ack=True)
    channel.start_consuming()

if __name__ == "__main__":
    thread = threading.Thread(target=consume, daemon=True)
    thread.start()

    app.run(debug=True)