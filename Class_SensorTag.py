from bluepy.btle import UUID, Peripheral, DefaultDelegate, AssignedNumbers
import struct

# Klasse übernommen von bluepy
# Weitere Detailinformationen unter: http://ianharvey.github.io/bluepy-doc/peripheral.html#peripheral
class SensorTag(Peripheral):

    #Instantierung
    def __init__(self):
        Peripheral.__init__(self,deviceAddr ='98:07:2D:27:F1:86', iface = 0 )
    # wenn deviceAddr angegeben wird, wird automatisch verbunden
    # iface aktiviert das Bluetooth Interface des Pis: /dev/hci0.

    # Methoden zum Aktivierung und Lesen der Sensoren bzw. Handles:

    # ----------Movement Sensor------------------
    def enableAllMovementAxis(self):
        # alle Achsen aktivieren, weil das speparate Aktivieren der Achsen die andere Achsen(bits) deaktiviert
        v = b'\xff\x00'  # ByteString von 11111111 (=alle bits)
        Peripheral.writeCharacteristic(self,handle = 0x003f,val= v, withResponse = True)

    def readGyroscope(self):
        data =  Peripheral.readCharacteristic(self,0x003c) # alle 18 bytes einlesen (zwei bytes je Achse)
        data = struct.unpack("<9h", data)[0:3]  # Umwandlung signed Integers(C) in Integer(Python) und Slicing
        x_y_z = tuple([ elem * (500.0 / 65536.0) for elem in data ]) # Umrechnung gemäß Doku
        return x_y_z

    def readAccelerometer(self):
        data =  Peripheral.readCharacteristic(self,0x003c) # alle 18 bytes einlesen (zwei bytes je Achse)
        data = struct.unpack("<9h", data)[3:6] # Umwandlung signed Integers(C) in Integer(Python) und Slicing
        x_y_z = tuple([ elem * (4.0 / 32768.0) for elem in data ]) # Umrechnung gemäß Doku mit Acc.- Range 4G
        return x_y_z

    def readMagnetometer(self):
        data =  Peripheral.readCharacteristic(self,0x003c) # alle 18 bytes einlesen (zwei bytes je Achse)
        data = struct.unpack("<9h", data)[6:7] # Umwandlung signed Integers(C) in Integer(Python) und Slicing
        data = data[0] # Umwandlung Tuple in Int
        return data


    # -----------Optical Sensor------------------------
    def enableLight(self):
        Peripheral.writeCharacteristic(self,handle = 0x0047,val= b'\x01', withResponse = True)

    def readLight(self):
        data =  Peripheral.readCharacteristic(self,0x0044)
        data = struct.unpack('<h', data) [0]
        m = data & 0xFFF;
        e = (data & 0xF000) >> 12;
        return ("{:6.2f}".format(0.01 * (m << e)))

    # -----------Humidity Sensor-------------------------
    def enableHumidity(self):
        Peripheral.writeCharacteristic(self,handle = 0x002f,val= b'\x01', withResponse = True)

    def readHumidity(self):
        data =  Peripheral.readCharacteristic(self,0x002c)
        (rawT, rawH) = struct.unpack('<HH', data)
        RH = (rawH / 65536.0) * 100.0
        return ("{:4.2f}".format(RH))

    def readTemperature(self):
        data =  Peripheral.readCharacteristic(self,0x002c)
        (rawT, rawH) = struct.unpack('<HH', data)
        temp = (rawT / 65536.0) * 165.0 -40.0
        return ("{:4.2f}".format(temp))

    # -----------Barometer Sensor-------------------------
    def enableBarometer(self):
        Peripheral.writeCharacteristic(self,handle = 0x0037,val= b'\x01', withResponse = True)

    def readBarometer(self):
        data =  Peripheral.readCharacteristic(self,0x0034)
        #  two 24-bit unsigned integers: the temperature in bytes 0-2, the pressure in bytes 3-5
        (tL,tM,tH,pL,pM,pH) = struct.unpack('<6B', data)
        temp = (tH*65536 + tM*256 + tL) / 100.0 # nicht im return statement,Temperatur kommt vom Feuchtigkeitssensor
        press = (pH*65536 + pM*256 + pL) / 100.0
        return ("{:6.2f}".format(temp,press))

    # -------------Battery Status------------------
    def readBattery(self):
        data =  Peripheral.readCharacteristic(self,0x001e)
        data = ord(data)
        return ("{}".format(data))


    #--------------Fuer IoT-Projekt nicht benötigt------------------
    def enableAccelerometer(self):
        v= b'8\x01' # aktiviert nur Beschleunigungs-Achsen
        Peripheral.writeCharacteristic(self,handle = 0x003f,val= v, withResponse = True)

    def enableGyroscope(self):
        v =b'\x07\x00' # aktiviert nur Gyroskop-Achsen
        Peripheral.writeCharacteristic(self,handle = 0x003f,val= v, withResponse = True)
