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

////////////////////

#include <wifi.h>
#include <format.h>
#include <ESP8266HTTPClient.h>
#include <AsyncElegantOTA.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <ErriezDHT22.h>

// Configure ID of the space
int space_id = 3;

// Set relay pins
const int RelayHeating = 15;
const int RelayLighting = 13;
const int RelayDehumidifier = 12;
const int RelayVentilation = 14;

// Sent goal
const int goal_humidity_value = 50 * 10;
const int goal_humidity_offset = 10 * 10;
const int goal_temperature_value = 22 * 10;
const int goal_temperature_offset = 2 * 10;
const int cycle_time_default = 20 * 60000;
const int cycle_time_offset = 10 * 60000;
const int ventilator_percentage_default = 30;
const int ventilator_percentage_offset = 10;
const int heater_percentage_default = 15;
const int heater_percentage_offset = 5;

int cycle_time;
int ventilator_percentage;
int heater_percentage;

// Control status boolean for power
int power_heating = LOW;
int power_lighting = LOW;
int power_dehumidifier = LOW;
int power_ventilation = LOW;

// NTP time client
WiFiUDP ntpUDP;
const long utcOffsetInSeconds = 7200;
NTPClient timeClient(ntpUDP, "pool.ntp.org", utcOffsetInSeconds);

// DHT22
#define DHT22_PIN 4 // PIN_D2
DHT22 dht22 = DHT22(DHT22_PIN);

// Global values
int16_t TEMPERATURE;
int16_t HUMIDITY;

// minute loop
bool minute_loop_has_run = false;
int8_t last_second = 0;

// climate loop control
unsigned long time_climate_cycle = 0;
unsigned long time_ventilator_control = ULONG_MAX;
unsigned long time_heater_control = ULONG_MAX;

void set_climate_cycle(int16_t temperature, int16_t humidity)
{
    cycle_time = cycle_time_default;
    ventilator_percentage = ventilator_percentage_default;
    heater_percentage = heater_percentage_default;
    if (humidity == ~0 or temperature == ~0) return;
    bool test_too_cold = temperature <= goal_temperature_value - goal_temperature_offset;
    if (temperature >= goal_temperature_value + goal_temperature_offset)
    {
        cycle_time += cycle_time_offset;
    }
    else if (test_too_cold)
    {
        cycle_time -= cycle_time_offset;
    }
    if (humidity >= goal_humidity_value + goal_humidity_offset)
    {
        ventilator_percentage += ventilator_percentage_offset;
        if (test_too_cold) heater_percentage += heater_percentage_offset;
    }
    else if (humidity <= goal_humidity_value - goal_humidity_offset)
    {
        ventilator_percentage -= ventilator_percentage_offset;
        if (test_too_cold) heater_percentage -= heater_percentage_offset;
    }
}

void control_lighting()
{
    int8_t hour = timeClient.getHours();
    String hoursStr = hour < 10 ? F("0") + String(hour) : String(hour);
    hour = hoursStr.toInt();
    power_lighting = (hour >= 1 and hour < 7) ? LOW : HIGH;
    digitalWrite(RelayLighting, power_lighting);
}

void send_data(String json_string)
{
    if (WiFi.status() == WL_CONNECTED)
    {
        WiFiClient client;
        HTTPClient http;

        http.begin(client, F("http://api.tuinbouwer.ga/sensor_api/v1/"));
        http.addHeader(F("Content-Type"), F("application/json"));

        int httpCode = http.POST(json_string);
        Serial.print(F("Send data status code: "));
        Serial.println(httpCode);

        http.end();
    }
    else
    {
        Serial.println(F("Error in WiFi connection"));
    }
}

void main_method(bool send_values)
{
    if (!dht22.available())
    {
        Serial.println(F("DHT22 not available."));
    }
    int16_t temperature = dht22.readTemperature();
    int16_t humidity = dht22.readHumidity();
    TEMPERATURE = temperature;
    HUMIDITY = humidity;

    // control_temperature(temperature);
    // control_humidity(humidity);
    control_lighting();

    Serial.println(format_status(timeClient.getFormattedTime(), temperature, humidity, power_heating, power_lighting, power_dehumidifier, power_ventilation, cycle_time, ventilator_percentage, heater_percentage));

    if (send_values and temperature != ~0 and humidity != ~0)
    {
        String json_string = format_sensor_data_json(space_id, temperature, humidity);
        send_data(json_string);
    }
}

////////////////////

void setup()
{
    pinMode(LED_BUILTIN, OUTPUT);
    pinMode(RelayHeating, OUTPUT);
    pinMode(RelayLighting, OUTPUT);
    pinMode(RelayDehumidifier, OUTPUT);
    pinMode(RelayVentilation, OUTPUT);

    Serial.begin(115200);
    while (!Serial)
        ;
    delay(200);

    setup_wifi();

    timeClient.begin();
    timeClient.update();

    webServer.on("/", HTTP_GET, [](AsyncWebServerRequest *request)
                 { request->send(200, F("text/plain"), format_status(timeClient.getFormattedTime(), TEMPERATURE, HUMIDITY, power_heating, power_lighting, power_dehumidifier, power_ventilation, cycle_time, ventilator_percentage, heater_percentage)); });
    webServer.on("/cycle", HTTP_GET, [](AsyncWebServerRequest *request)
                 { request->send(200, F("text/plain"), format_cycle_time(time_climate_cycle, cycle_time, time_ventilator_control, ventilator_percentage, time_heater_control, heater_percentage)); });
    webServer.on("/json", HTTP_GET, [](AsyncWebServerRequest *request)
                 { request->send(200, F("application/json"), format_sensor_data_json(space_id, TEMPERATURE, HUMIDITY)); });

    AsyncElegantOTA.begin(&webServer);
    webServer.begin();

    main_method(false);
}

void loop()
{
    check_wifi_status();

    int current_second = timeClient.getSeconds();
    if (!minute_loop_has_run and current_second == 0)
    {
        minute_loop_has_run = true;
        main_method(true);
    }
    else if (last_second != current_second and current_second != 0)
    {
        Serial.print(current_second);
        Serial.print(F(" "));
        Serial.println(format_cycle_time(time_climate_cycle, cycle_time, time_ventilator_control, ventilator_percentage, time_heater_control, heater_percentage));
        last_second = current_second;
        minute_loop_has_run = false;
    }

    unsigned long currentMillis = millis();
    if (currentMillis >= time_ventilator_control)
    {
        time_ventilator_control = ULONG_MAX;
        Serial.println("stop ventilator, start heater");

        power_ventilation = LOW;
        power_heating = HIGH;
        digitalWrite(RelayVentilation, power_ventilation);
        digitalWrite(RelayHeating, power_heating);
    }
    else if (currentMillis >= time_heater_control)
    {
        time_heater_control = ULONG_MAX;

        Serial.println("stop heater");
        power_heating = LOW;
        digitalWrite(RelayHeating, power_heating);
    }
    else if (currentMillis >= time_climate_cycle)
    {
        Serial.println("start ventilation");
        int16_t temperature = dht22.readTemperature();
        int16_t humidity = dht22.readHumidity();
        set_climate_cycle(temperature, humidity);

        time_ventilator_control = currentMillis + (cycle_time / 100 * ventilator_percentage);
        time_heater_control = time_ventilator_control + (cycle_time / 100 * heater_percentage);
        time_climate_cycle = currentMillis + cycle_time;

        power_ventilation = HIGH;
        digitalWrite(RelayVentilation, power_ventilation);
    }
}