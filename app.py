from flask import Flask
import paho.mqtt.client as mqtt
import uuid
from flask_cors import CORS, cross_origin
import ssl
import sys

color = "#FFFFFF"

app = Flask(__name__)

topic2 = 'IDD/bar'
topic3 = 'IDD/detect'
port = 5000
topic = 'IDD/#'
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['development'] = True
app.config['debug'] = True

def on_connect(client, userdata, flags, rc):
    client.subscribe(topic)
    client.publish(topic3, "STARTING SERVER")
    client.publish(topic3, "CONNECTED")


def on_message(client, userdata, msg):
    global color
    if (msg.topic == "IDD/bar") and float(msg.payload.decode('UTF-8')) < 0.1:
        color = "#FFFFFF"
    if (msg.topic == "IDD/bar") and float(msg.payload.decode('UTF-8')) >= 0.1:
        color = "#DDDDDD"
    print(f"topic: {msg.topic} msg: {msg.payload.decode('UTF-8')}", file=sys.stderr)

@app.route('/dtoc/<d>')
@cross_origin()
def d_c(d):
    global color
    if (float(d) < 0.1):
        color = "#FFFFFF"
    elif (float(d) > 0.1):
        color = "#AAAAAA"
    print(color)
    return color


@app.route('/')
@cross_origin()
def hello_world():
    global color
    print(color)
    return color

if __name__ == '__main__':
    client = mqtt.Client(str(uuid.uuid1()))
    client.tls_set(cert_reqs=ssl.CERT_NONE)
    client.username_pw_set('idd', 'device@theFarm')
    # attach out callbacks to the client
    client.on_connect = on_connect
    client.on_message = on_message
    #connect to the broker
    client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)
    client.loop_start()
    app.run(host='0.0.0.0', port=port, debug=True)
