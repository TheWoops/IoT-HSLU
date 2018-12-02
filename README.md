# Repository zum IoT-Projekt HSLU (Gruppe 3)


### Python-Skripte für Sensoranbindung

- Class_SensorTag.py beeinhaltet die Objektorientierte Abbildung des TI SensorTags
- SensorMain.py beeinhaltet das Hauptprogramm zu Lesen der Sensorwerte und Senden der Daten an den MQTT-Broker

*Hinweis: Beide Skripte müssen sich im Verzeichnis bluepy/bluepy befinden, um korrekt ausgeführt werden zu können.*

### Voraussetzungen:

- Python3 Interpreter auf dem RaspberryPi
- Library [Bluepy](https://github.com/IanHarvey/bluepy) installiert (= Python interface to Bluetooth LE on Linux)
- Paho MQTT Python client library installiert
