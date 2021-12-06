from flask import Flask
import paho.mqtt.client as mqtt
import uuid
from flask_cors import CORS, cross_origin
import ssl
import sys
from flask_sqlalchemy import SQLAlchemy

color = "#FFFFFF"
d = 0

app = Flask(__name__)

topic2 = 'IDD/bar'
topic3 = 'IDD/detect'
port = 5000
topic = 'IDD/#'
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['development'] = True
app.config['debug'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hbwpqdzjkhdlax:6af94ed9702af551f17bc044ede5430e8c02af239d8a48d7c44f56ebc70f8a48@ec2-3-217-129-39.compute-1.amazonaws.com:5432/d46ssoe1tblupj'
db = SQLAlchemy(app)

class Light(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lighting = db.Column(db.Float)

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

@app.route('/dtoc/<dis>')
@cross_origin()
def d_c(dis):
    global color
    global d
    print(d)
    l = Light.query.get(1)
    l.lighting = float(dis)
    db.session.commit()
    return str(dis)


@app.route('/')
@cross_origin()
def hello_world():
    global color
    global d
    print(color, d)
    return str(Light.query.get(1).lighting)

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
