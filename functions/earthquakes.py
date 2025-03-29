from datetime import datetime
import json
from json import JSONDecodeError
from flask import jsonify
from firebase_admin import firestore

def get_earthquakes_mock():
    try:
        with open('mocks/earth_quake.json', 'r') as f:
            earthquake_data = json.load(f)
            return jsonify(earthquake_data=earthquake_data)
    except FileNotFoundError:
        return jsonify(error='Earthquake data not found'), 404
    except JSONDecodeError:
        return jsonify(error='Invalid JSON format'), 500
    except Exception as e:
        return jsonify(error=f'An unexpected error occurred: {str(e)}'), 500

def get_earthquake_latest():
    firestore_client = firestore.client()
    earthquakes_collection = firestore_client.collection('earthquakes')
    earthquakes_docs = earthquakes_collection.stream()
    earthquakes_data = []
    for doc in earthquakes_docs:
        data = doc.to_dict()
        earthquakes_data.append(data)
    if earthquakes_data:
        return earthquakes_data[0]
    else:
        return None

def occur_earthquake():
    pass