#!/bin/python3

from flask import Flask, request, jsonify
import redis

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

if __name__ == "__main__":
    app.run(debug=True)