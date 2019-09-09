# Repository zum IoT-Projekt HSLU


### Python-Skripte für Sensoranbindung eines [TISensorTags](http://www.ti.com/ww/en/wireless_connectivity/sensortag/)

- Class_SensorTag.py beeinhaltet die Objektorientierte Abbildung des TI SensorTags
- SensorMain.py beeinhaltet das Hauptprogramm zu Lesen der Sensorwerte und Senden der Daten an den MQTT-Broker

*Hinweis: Beide Skripte müssen sich im Verzeichnis bluepy/bluepy befinden, um korrekt ausgeführt werden zu können.*

### Voraussetzungen:

- Python3 Interpreter auf dem RaspberryPi
- Library [Bluepy](https://github.com/IanHarvey/bluepy) installiert (= Python interface für Bluetooth LE on Linux)
- [Paho MQTT Python client library](https://pypi.org/project/paho-mqtt/) installiert
- RaspberryPi im Hochschulnetz (lokal of VPN)
