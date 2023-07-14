from flask import Flask, render_template, request
import paho.mqtt.client as mqtt

app = Flask(__name__)

# MQTT connection details
mqtt_broker = "broker.example.com"
mqtt_port = 1883

# MQTT connection status
mqtt_connected = False

# MQTT on_connect event
def on_connect(client, userdata, flags, rc):
    global mqtt_connected
    if rc == 0:
        mqtt_connected = True
    else:
        mqtt_connected = False

mqtt_client = mqtt.Client()

# Bind MQTT on_connect event
mqtt_client.on_connect = on_connect

@app.route("/")
def index():
    return render_template("mqtt_connection.html")

@app.route("/connect", methods=["POST"])
def connect():
    global mqtt_connected
    if mqtt_connected:
        return "Already connected to MQTT broker"
    
    client_id = request.form.get("client_id")
    mqtt_client.connect(mqtt_broker, mqtt_port)
    mqtt_client.loop_start()
    
    return "Connected to MQTT broker"

@app.route("/disconnect", methods=["POST"])
def disconnect():
    global mqtt_connected
    if not mqtt_connected:
        return "Not connected to MQTT broker"
    
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    mqtt_connected = False
    
    return "Disconnected from MQTT broker"

if __name__ == "__main__":
    app.run()
