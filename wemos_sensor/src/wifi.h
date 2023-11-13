#ifndef WIFI_H
#define WIFI_H
#include <Arduino.h>
#include <FS.h>
#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#include <DNSServer.h>
#include <ESP8266WiFiMulti.h>
#include <ESPAsyncWebServer.h>

void setup_wifi();
void check_wifi_status();
extern AsyncWebServer webServer;

#endif