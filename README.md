# Tuinbouwer Sensor
Software application to run on Raspberry Pi sensor instance to collect data and send to Tuinbouwer Server API.

## Command line
To start application run:
```
tuinbouwer_sensor
```

## Sensor
Read humidity and temperature from DHT22 sensor connected to pin 4.

## Environ variables
The following example variables should be placed in `.env`.
```
AUTHORIZATION=PLACEHOLDER
API_URL='http://localhost:5000/sensor_api/v1/'
```

* `AUTHORIZATION` authentication key, currently not used
* `API_URL` url to POST sensor information to
