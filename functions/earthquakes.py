import json
from json import JSONDecodeError
from flask import jsonify

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

def occur_earthquake():
    pass