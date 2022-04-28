/*>
    Async_AutoConnect_ESP8266_minimal.ino
    For ESP8266 / ESP32 boards
    Built by Khoi Hoang https://github.com/khoih-prog/ESPAsync_WiFiManager
    Licensed under MIT license
 */

#include <Arduino.h>
#include <ESPAsync_WiFiManager.h>
#include <AsyncElegantOTA.h>

AsyncWebServer webServer( 80 );

DNSServer dnsServer;

void setup()
{
    Serial.begin( 115200 );
    while ( !Serial ); delay( 200 );
    Serial.print( "\nStarting Async_AutoConnect_ESP8266_minimal on " + String( ARDUINO_BOARD ) );
    Serial.println( ESP_ASYNC_WIFIMANAGER_VERSION );
    ESPAsync_WiFiManager ESPAsync_wifiManager( &webServer, &dnsServer, "AutoConnectAP" );
    ESPAsync_wifiManager.autoConnect( "AutoConnectAP" );
    if ( WiFi.status() == WL_CONNECTED ) {
        Serial.print( F( "Connected. Local IP: " ) );
        Serial.println( WiFi.localIP() );
    }
    else {
        Serial.println( ESPAsync_wifiManager.getStatus( WiFi.status() ) );
    }

    webServer.on( "/", HTTP_GET, [](AsyncWebServerRequest *request ) {
        request->send( 200, "text/plain", "Hi! I am ESP32." );
    });

    AsyncElegantOTA.begin( &webServer ); // Start ElegantOTA
    webServer.begin();
    Serial.println( "Http server started" );

}

void loop() {

}