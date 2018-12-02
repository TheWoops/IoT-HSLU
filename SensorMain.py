#!/usr/bin/env/python
# Pfad zum Dictionary, wo der Python-Interpreter eingetragen ist.
# Dies erspart den zusätzlichen Aufruf des Interpreters bei Skriptaufruf über die Kommandozeile

# Definitionen Funktionen, welche der Pi/das Skript ausführt
def on_connect(client, userdata, flags, rc):
            # Einführung einer Variable Connected, welche angibt, ob der Pi/Sensor zum MQTT-broker verbunden ist.

            if rc == 0:                         # rc gibt den Verbindungsstatus an. rc=0 verbunden, alles andere false
                global Connected                # Variable Connected in Funktion verfügbar machen
                Connected = True                #Signal connection
                print("Connected to broker")
                print("")
            else:
                print("Connection failed")

def connect_to_mqtt():
            global Connected
            Connected = False # Inital ist Verbindung nicht aktiv, also false.
            broker= "143.93.197.81"   # IWILR3-6
            sensor_topic = "Factory/SensorCC2650/Measurement"

            # Neue Client-Instanz mit unique Identifier "client"
            client = paho.Client("client")
            print("   Topic ist :", sensor_topic)
            client.on_connect = on_connect

            # Verbindungsaufbau um Broker, welcher Default auf Port 1883 läuft
            client.connect(broker,port=1883)
            # Die Methode loop_start startet einen Thread, welcher sich um die Verbindung zum Broker
            # und das Senden/Empfangen der Daten kümmert
            client.loop_start()

            # Verbindungsaufbau kann dauern.
            # Erst wenn die Variable Connected von der Methode on_connect auf True gesetzt wird, kann "gepublisht" werden
            # Bis dahin loopt das Hauptprogramm durch eine Schleife, welche ein Verzögerung erzeugt
            while Connected !=True:
                time.sleep(0.1)

            try:
                while True:
                    data = {
                                'Temperatur'        : SensorTag.readTemperature(),
                                'Relative Feuchte'  : SensorTag.readHumidity(),
                                'Beschleunigung'    : SensorTag.readAccelerometer(),
                                'Magnetometer'      : SensorTag.readMagnetometer(),
                                'Barometer'         : SensorTag.readBarometer(),
                                'Gyroskop'          : SensorTag.readGyroscope(),
                                'Helligkeit'        : SensorTag.readLight(),
                                'Batterie'          : SensorTag.readBattery(),
                                'Zeitstempel'       : time.strftime("%d.%m.%Y %H:%M:%S"),
                            }

                    payload=json.dumps(data)
                    print(payload)
                    print("")
                    client.publish(sensor_topic, payload, retain=True)  # retain=True um Message als retained message beim Broker zu hinterlegen
                    time.sleep(t) # Sobald Variable Connected=True wird alle 5 Sekunden gesendet

            except KeyboardInterrupt:
                client.disconnect()
                client.loop_stop()


# Hier beginnt der eigentliche Code, zunächst mit einigen Datenimporten
# Details zu den Importen im Projektbericht
from Class_SensorTag import *
import json
import time
import paho.mqtt.client as paho
import paho.mqtt.publish as publish
import argparse

# Parser, welche als optionales Argument ein Float entgegen nimmt.
# Festgelegt kann hiermit der Sendeabstand des Sensors in Sekunden
parser = argparse.ArgumentParser(); # Instantierung Parser
parser.add_argument("-t", action="store", type=float, default = 5.0)
args = parser.parse_args()
t = args.t
print("Sendeabstand {} Sekunden".format(t))
print("")

# Output Kommandozeile mit Bluetooth Adresse des Sensors
print('Connecting to ' + '98:07:2D:27:F1:86')

# Erstellung eines Objekts der Klasse SensorTag
# Sobald die Verbindung aktiv ist, können Services und Charakteristika des Sensors gelesen oder geschrieben werden.
SensorTag = SensorTag()
print("Verbindung erfolgereich hergestellt")
print(" ")

print("Aktivierung Sensoren des CC2650...")
SensorTag.enableLight();
SensorTag.enableHumidity();
SensorTag.enableAllMovementAxis(); # ativiert Beschleunigungsmesser, Gyroskop und Kompass
SensorTag.enableBarometer();

time.sleep(1.0) # Kleine Zeitverzögerung um sicherzustellen, dass Sensoren die Aktivierungssignale verarbeitet haben

# Erste Abfrage Sensoren und Ausgabe auf Kommandozeile
print("Luftfeuchtigkeit: {}".format(SensorTag.readHumidity()))
print("Temperatur: {}".format(SensorTag.readTemperature()))
print("Beschleunigung: {}".format(SensorTag.readAccelerometer()))
print("Barometer: {}".format(SensorTag.readBarometer()))
print("Gyroskop: {}".format(SensorTag.readGyroscope()))
print("Helligkeit: {}".format(SensorTag.readLight()))
print("Batterie: {}".format(SensorTag.readBattery()))
print("Zeitstempel: {}".format(time.strftime("%d.%m.%Y %H:%M:%S")))

print(" ")
print("Verbindungsaufbau zum MQTT-Broker...")
connect_to_mqtt()
