/*
 * Four Chanel Relay Climate Control
 *
 * Manage climate using DHT22, connected to port 2
 *
 * D0  GPIO 16
 * D1  GPIO 5
 * D2  GPIO 4
 * D3  GPIO 0
 * D4  GPIO 2
 * D5  GPIO 14
 * D6  GPIO 12
 * D7  GPIO 13
 * D8  GPIO 15
 * RX  GPIO 3
 * TX  GPIO 1
 * A0  ADC0
 * 
 *  Async_AutoConnect_ESP8266_minimal.ino
 *  For ESP8266 / ESP32 boards
 *  Built by Khoi Hoang https://github.com/khoih-prog/ESPAsync_WiFiManager
 *  Licensed under MIT license
 */

#include <Arduino.h>
#include <ESPAsync_WiFiManager.h>
#include <AsyncElegantOTA.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <ErriezDHT22.h>

// Set relay pins
const int RelayHeating = 15;
const int RelayLighting = 13;
const int RelayDehumidifier = 12;
const int RelayVentilation = 14;

// Sent goal 
const int goal_temperature_value = 22 * 10;
const int goal_temperature_offset = 2 * 10;
const int goal_humidity_value = 70 * 10;
const int goal_humidity_offset = 10 * 10;

// Control status boolean for power
int power_heating = LOW;
int power_lighting = LOW;
int power_dehumidifier = LOW;
int power_ventilation = LOW;

AsyncWebServer webServer(80);

DNSServer dnsServer;

WiFiUDP ntpUDP;
const long utcOffsetInSeconds = 7200;
NTPClient timeClient(ntpUDP, "pool.ntp.org", utcOffsetInSeconds);

#define DHT22_PIN 2
DHT22 dht22 = DHT22(DHT22_PIN);

// Global values
int16_t TEMPERATURE;
int16_t HUMIDITY;

unsigned long previousMillis = 0;
bool has_not_run = true;
int8_t last_second = 0;

int getHours24(int hours) {
    String hoursStr = hours < 10 ? "0" + String(hours) : String(hours);
    return hoursStr.toInt();
}

void control_temperature(int16_t temperature)
{
    if (temperature != ~0 or (power_heating and temperature >= goal_temperature_value + goal_temperature_offset))
    {
        power_heating = LOW;
    }
    else if (not power_heating and temperature <= goal_temperature_value + goal_temperature_offset)
    {
        power_heating = HIGH;
    }
}

void control_humidity(int16_t humidity)
{
    if (humidity == ~0) {
        power_dehumidifier = LOW;
        power_ventilation = HIGH;
    }
    else
    {
        if (not power_ventilation)
        {
            if (humidity >= goal_humidity_value + goal_humidity_offset)
            {
                power_ventilation = HIGH;
            }
        }
        else if (power_dehumidifier)
        {
            if (humidity <= goal_humidity_value - goal_humidity_offset)
            {
                power_dehumidifier = LOW;
            }
        }
        else
        {
            if (humidity >= goal_humidity_value + goal_humidity_offset)
            {
                power_dehumidifier = HIGH;
            }
            else if (humidity <= goal_humidity_value - goal_humidity_offset) {
                power_ventilation = LOW;
            }
        }
    }
}

void control_lighting()
{
    int8_t hour = getHours24(timeClient.getHours());
    power_lighting = (hour >= 1 and hour < 7) ? LOW : HIGH;
}

String format_climate( int16_t temperature, int16_t humidity )
{
    String climate_str = F("Temperature: ");
    if (temperature == ~0) {
        climate_str = climate_str + F("Error");
    }
    else {
        climate_str = climate_str
            + String(temperature / 10) + F(".") + String(temperature % 10) + F(" *C");
    }
    climate_str = climate_str + F(" Humidity: ");
    if (humidity == ~0) {
        climate_str = climate_str + F("Error");
    } else {
        climate_str = climate_str
            + String(humidity / 10) + F(".") + String(humidity % 10) + F(" %");
    }
    return climate_str;
}

void print_climate(int16_t temperature, int16_t humidity)
{
    Serial.print(timeClient.getFormattedTime());
    Serial.print(F(" "));
    Serial.println(format_climate(temperature, humidity));
}

String format_controls() 
{
    return F("Heating: ") + String(power_heating)
        + F(" Lighting: ") + String(power_lighting)
        + F(" Dehumidifier: ") + power_dehumidifier
        + F(" Ventilation: ") + power_ventilation;
}

void print_controls()
{
    Serial.print(timeClient.getFormattedTime());
    Serial.print(F(" "));
    Serial.println(format_controls());
}

void setup()
{
    Serial.begin(115200);
    Serial.println(F("Starting application"));

    pinMode(RelayHeating, OUTPUT);
    pinMode(RelayLighting, OUTPUT);
    pinMode(RelayDehumidifier, OUTPUT);
    pinMode(RelayVentilation, OUTPUT);

    ESPAsync_WiFiManager ESPAsync_wifiManager(&webServer, &dnsServer, "AutoConnectAP");
    ESPAsync_wifiManager.autoConnect("AutoConnectAP");
    if (WiFi.status() == WL_CONNECTED) {
        Serial.print(F("Connected. Local IP: "));
        Serial.println(WiFi.localIP());
    }
    else {
        Serial.println(ESPAsync_wifiManager.getStatus(WiFi.status()));
    }

    timeClient.begin();
    timeClient.update();

    webServer.on("/", HTTP_GET, [](AsyncWebServerRequest *request) {
        request->send(200, "text/plain", timeClient.getFormattedTime() 
                + F(" ")
                + format_climate(TEMPERATURE, HUMIDITY)
                + F(" ")
                + format_controls()
            );
    });

    AsyncElegantOTA.begin(&webServer);
    webServer.begin();
}

void loop() {
    int current_second = timeClient.getSeconds();

    if (current_second == 0 and has_not_run) {
        has_not_run = false;
        if (dht22.available()) {
            Serial.println(F("DHT22 not available."));
        }

        int16_t temperature = dht22.readTemperature();
        int16_t humidity = dht22.readHumidity();
        TEMPERATURE = temperature;
        HUMIDITY = humidity;

        print_climate(temperature, humidity);

        control_temperature(temperature);
        control_lighting();
        control_humidity(humidity);

        digitalWrite(RelayHeating, power_heating);
        digitalWrite(RelayLighting, power_lighting);
        digitalWrite(RelayVentilation, power_ventilation);
        digitalWrite(RelayDehumidifier, power_dehumidifier);

        print_controls();
    }
    else if (last_second != current_second and current_second != 0) {
        Serial.println(current_second);
        last_second = current_second; 
        has_not_run = true;
    }
}