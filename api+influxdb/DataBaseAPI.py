from flask import Flask, request, jsonify
from influxdb import InfluxDBClient

app = Flask(__name__)
influx_client = InfluxDBClient(host="influxdb", database='DHBW_Blickbox')

@app.route('/iot/pingdb', methods=['GET'])
def pingthis():
    try:
        influx_client.ping()
        return jsonify({"message": "Verbingung zur Datenbank steht"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/iot/api/insert/temperature', methods=['POST'])
def insert_temperature():
    try:
        data = request.json
        temperature = data['temperature']
        json_body = [
            {
                "measurement": "temperature",
                "fields": {
                    "value": temperature
                }
            }
        ]
        influx_client.write_points(json_body)
        return jsonify({"message": "Daten erfolgreich eingefügt"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
