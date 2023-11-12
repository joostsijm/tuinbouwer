"""Read from sensor"""

import Adafruit_DHT


DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

def read_sensor():
    """Read sensor information"""
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is None:
        humidity = 0
    if temperature is None:
        temperature = 0
    return humidity, temperature
