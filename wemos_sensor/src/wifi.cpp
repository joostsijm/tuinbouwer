#include "wifi.h"

AsyncWebServer webServer(80);

ESP8266WiFiMulti wifiMulti;

#include <LittleFS.h>
FS *filesystem = &LittleFS;
#define FileFS LittleFS
#define FS_Name "LittleFS"

#define ESP_getChipId() (ESP.getChipId())

#define LED_ON LOW
#define LED_OFF HIGH

// PIN_D0 can't be used for PWM/I2C
#define PIN_D0 16 // Pin D0 mapped to pin GPIO16/USER/WAKE of ESP8266. This pin is also used for Onboard-Blue LED. PIN_D0 = 0 => LED ON
#define PIN_D1 5  // Pin D1 mapped to pin GPIO5 of ESP8266
#define PIN_D2 4  // Pin D2 mapped to pin GPIO4 of ESP8266
#define PIN_D3 0  // Pin D3 mapped to pin GPIO0/FLASH of ESP8266
#define PIN_D4 2  // Pin D4 mapped to pin GPIO2/TXD1 of ESP8266
#define PIN_LED 2 // Pin D4 mapped to pin GPIO2/TXD1 of ESP8266, NodeMCU and WeMoS, control on-board LED
#define PIN_D5 14 // Pin D5 mapped to pin GPIO14/HSCLK of ESP8266
#define PIN_D6 12 // Pin D6 mapped to pin GPIO12/HMISO of ESP8266
#define PIN_D7 13 // Pin D7 mapped to pin GPIO13/RXD2/HMOSI of ESP8266
#define PIN_D8 15 // Pin D8 mapped to pin GPIO15/TXD2/HCS of ESP8266
// Don't use pins GPIO6 to GPIO11 as already connected to flash, etc. Use them can crash the program
// GPIO9(D11/SD2) and GPIO11 can be used only if flash in DIO mode ( not the default QIO mode)
#define PIN_D11 9  // Pin D11/SD2 mapped to pin GPIO9/SDD2 of ESP8266
#define PIN_D12 10 // Pin D12/SD3 mapped to pin GPIO10/SDD3 of ESP8266
#define PIN_SD2 9  // Pin SD2 mapped to pin GPIO9/SDD2 of ESP8266
#define PIN_SD3 10 // Pin SD3 mapped to pin GPIO10/SDD3 of ESP8266
#define PIN_D9 3   // Pin D9 /RX mapped to pin GPIO3/RXD0 of ESP8266
#define PIN_D10 1  // Pin D10/TX mapped to pin GPIO1/TXD0 of ESP8266
#define PIN_RX 3   // Pin RX mapped to pin GPIO3/RXD0 of ESP8266
#define PIN_TX 1   // Pin RX mapped to pin GPIO1/TXD0 of ESP8266
#define LED_PIN 16 // Pin D0 mapped to pin GPIO16 of ESP8266. This pin is also used for Onboard-Blue LED. PIN_D0 = 0 => LED ON

const char *CONFIG_FILE = "/ConfigSW.json";

// Function Prototypes
bool readConfigFile();
bool writeConfigFile();

// SSID and PW for Config Portal
String ssid = "ESP_" + String(ESP_getChipId(), HEX);

// SSID and PW for your Router
String Router_SSID;
String Router_Pass;

#define MIN_AP_PASSWORD_SIZE 8
#define SSID_MAX_LEN 32
#define PASS_MAX_LEN 64

typedef struct
{
    char wifi_ssid[SSID_MAX_LEN];
    char wifi_pw[PASS_MAX_LEN];
} WiFi_Credentials;

typedef struct
{
    String wifi_ssid;
    String wifi_pw;
} WiFi_Credentials_String;

#define NUM_WIFI_CREDENTIALS 2

// Assuming max 49 chars
#define TZNAME_MAX_LEN 50
#define TIMEZONE_MAX_LEN 50

typedef struct
{
    WiFi_Credentials WiFi_Creds[NUM_WIFI_CREDENTIALS];
    uint16_t checksum;
} WM_Config;

WM_Config WM_config;

#define CONFIG_FILENAME F("/wifi_cred.dat")

// Indicates whether ESP has WiFi credentials saved from previous session
bool initialConfig = false;

// Just use enough to save memory. On ESP8266, can cause blank ConfigPortal screen
// if using too much memory
#define USING_AFRICA false
#define USING_AMERICA false
#define USING_ANTARCTICA false
#define USING_ASIA false
#define USING_ATLANTIC false
#define USING_AUSTRALIA false
#define USING_EUROPE true
#define USING_INDIAN false
#define USING_PACIFIC false
#define USING_ETC_GMT false

IPAddress stationIP = IPAddress(0, 0, 0, 0);
IPAddress gatewayIP = IPAddress(192, 168, 2, 1);
IPAddress netMask = IPAddress(255, 255, 255, 0);

IPAddress dns1IP = gatewayIP;
IPAddress dns2IP = IPAddress(8, 8, 8, 8);
IPAddress APStaticIP = IPAddress(192, 168, 100, 1);
IPAddress APStaticGW = IPAddress(192, 168, 100, 1);
IPAddress APStaticSN = IPAddress(255, 255, 255, 0);

// Use from 0 to 4. Higher number, more debugging messages and memory usage.
#define _ESPASYNC_WIFIMGR_LOGLEVEL_ 3

#include <ESPAsync_WiFiManager.h>

// AsyncWebServer webServer(80);
DNSServer dnsServer;
ESPAsync_WiFiManager ESPAsync_wifiManager(&webServer, &dnsServer);

WiFi_AP_IPConfig WM_AP_IPconfig;
WiFi_STA_IPConfig WM_STA_IPconfig;

void initAPIPConfigStruct(WiFi_AP_IPConfig &in_WM_AP_IPconfig)
{
    in_WM_AP_IPconfig._ap_static_ip = APStaticIP;
    in_WM_AP_IPconfig._ap_static_gw = APStaticGW;
    in_WM_AP_IPconfig._ap_static_sn = APStaticSN;
}

void initSTAIPConfigStruct(WiFi_STA_IPConfig &in_WM_STA_IPconfig)
{
    in_WM_STA_IPconfig._sta_static_ip = stationIP;
    in_WM_STA_IPconfig._sta_static_gw = gatewayIP;
    in_WM_STA_IPconfig._sta_static_sn = netMask;
    in_WM_STA_IPconfig._sta_static_dns1 = dns1IP;
    in_WM_STA_IPconfig._sta_static_dns2 = dns2IP;
}

void displayIPConfigStruct(WiFi_STA_IPConfig in_WM_STA_IPconfig)
{
    LOGERROR3(F("stationIP ="), in_WM_STA_IPconfig._sta_static_ip, ", gatewayIP =", in_WM_STA_IPconfig._sta_static_gw);
    LOGERROR1(F("netMask ="), in_WM_STA_IPconfig._sta_static_sn);
    LOGERROR3(F("dns1IP ="), in_WM_STA_IPconfig._sta_static_dns1, ", dns2IP =", in_WM_STA_IPconfig._sta_static_dns2);
}

void configWiFi(WiFi_STA_IPConfig in_WM_STA_IPconfig)
{
    // Set static IP, Gateway, Subnetmask, DNS1 and DNS2. New in v1.0.5
    WiFi.config(in_WM_STA_IPconfig._sta_static_ip, in_WM_STA_IPconfig._sta_static_gw, in_WM_STA_IPconfig._sta_static_sn, in_WM_STA_IPconfig._sta_static_dns1, in_WM_STA_IPconfig._sta_static_dns2);
}

uint8_t connectMultiWiFi()
{
// For ESP8266, this better be 2200 to enable connect the 1st time
#define WIFI_MULTI_1ST_CONNECT_WAITING_MS 2200L
#define WIFI_MULTI_CONNECT_WAITING_MS 500L
    uint8_t status;
    LOGERROR(F("ConnectMultiWiFi with :"));
    if ((Router_SSID != "") && (Router_Pass != ""))
    {
        LOGERROR3(F("* Flash-stored Router_SSID = "), Router_SSID, F(", Router_Pass = "), Router_Pass);
        LOGERROR3(F("* Add SSID = "), Router_SSID, F(", PW = "), Router_Pass);
        wifiMulti.addAP(Router_SSID.c_str(), Router_Pass.c_str());
    }
    for (uint8_t i = 0; i < NUM_WIFI_CREDENTIALS; i++)
    {
        // Don't permit NULL SSID and password len < MIN_AP_PASSWORD_SIZE (8)
        if ((String(WM_config.WiFi_Creds[i].wifi_ssid) != "") && (strlen(WM_config.WiFi_Creds[i].wifi_pw) >= MIN_AP_PASSWORD_SIZE))
        {
            LOGERROR3(F("* Additional SSID = "), WM_config.WiFi_Creds[i].wifi_ssid, F(", PW = "), WM_config.WiFi_Creds[i].wifi_pw);
        }
    }
    LOGERROR(F("Connecting MultiWifi..."));
    int i = 0;
    status = wifiMulti.run();
    delay(WIFI_MULTI_1ST_CONNECT_WAITING_MS);
    while ((i++ < 20) && (status != WL_CONNECTED))
    {
        status = WiFi.status();
        if (status == WL_CONNECTED)
        {
            break;
        }
        else
        {
            delay(WIFI_MULTI_CONNECT_WAITING_MS);
        }
    }
    if (status == WL_CONNECTED)
    {
        LOGERROR1(F("WiFi connected after time: "), i);
        LOGERROR3(F("SSID:"), WiFi.SSID(), F(",RSSI="), WiFi.RSSI());
        LOGERROR3(F("Channel:"), WiFi.channel(), F(",IP address:"), WiFi.localIP());
    }
    else
    {
        LOGERROR(F("WiFi not connected"));
        ESP.reset();
    }
    return status;
}

void check_WiFi()
{
    if ((WiFi.status() != WL_CONNECTED))
    {
        Serial.println(F("\nWiFi lost. Call connectMultiWiFi in loop"));
        connectMultiWiFi();
    }
}

void check_wifi_status()
{
    static unsigned long checkwifi_timeout = 0;
    static unsigned long current_millis;
#define WIFICHECK_INTERVAL 1000L
    current_millis = millis();
    // Check WiFi every WIFICHECK_INTERVAL (1) seconds.
    if ((current_millis > checkwifi_timeout) || (checkwifi_timeout == 0))
    {
        check_WiFi();
        checkwifi_timeout = current_millis + WIFICHECK_INTERVAL;
    }
}

int calcChecksum(uint8_t *address, uint16_t sizeToCalc)
{
    uint16_t checkSum = 0;
    for (uint16_t index = 0; index < sizeToCalc; index++)
    {
        checkSum += *(((byte *)address) + index);
    }
    return checkSum;
}

bool loadConfigData()
{
    File file = FileFS.open(CONFIG_FILENAME, "r");
    LOGERROR(F("LoadWiFiCfgFile "));
    memset((void *)&WM_config, 0, sizeof(WM_config));
    memset((void *)&WM_STA_IPconfig, 0, sizeof(WM_STA_IPconfig));
    if (file)
    {
        file.readBytes((char *)&WM_config, sizeof(WM_config));
        file.readBytes((char *)&WM_STA_IPconfig, sizeof(WM_STA_IPconfig));

        file.close();
        LOGERROR(F("OK"));

        if (WM_config.checksum != calcChecksum((uint8_t *)&WM_config, sizeof(WM_config) - sizeof(WM_config.checksum)))
        {
            LOGERROR(F("WM_config checksum wrong"));
            return false;
        }
        displayIPConfigStruct(WM_STA_IPconfig);
        return true;
    }
    else
    {
        LOGERROR(F("failed"));
        return false;
    }
}

void saveConfigData()
{
    File file = FileFS.open(CONFIG_FILENAME, "w");
    LOGERROR(F("SaveWiFiCfgFile "));
    if (file)
    {
        WM_config.checksum = calcChecksum((uint8_t *)&WM_config, sizeof(WM_config) - sizeof(WM_config.checksum));
        file.write((uint8_t *)&WM_config, sizeof(WM_config));
        displayIPConfigStruct(WM_STA_IPconfig);
        file.write((uint8_t *)&WM_STA_IPconfig, sizeof(WM_STA_IPconfig));
        file.close();
        LOGERROR(F("OK"));
    }
    else
    {
        LOGERROR(F("failed"));
    }
}

bool readConfigFile()
{
    File file = FileFS.open(CONFIG_FILE, "r");
    if (!file)
    {
        Serial.println(F("Configuration file not found"));
        return false;
    }
    else
    {
        size_t size = file.size();
        std::unique_ptr<char[]> buf(new char[size + 1]);
        file.readBytes(buf.get(), size);
        file.close();

        DynamicJsonDocument json(1024);
        auto deserializeError = deserializeJson(json, buf.get());
        if (deserializeError)
        {
            Serial.println(F("JSON parseObject() failed"));
            return false;
        }
        serializeJson(json, Serial);
    }
    Serial.println(F("\nConfig file was successfully parsed"));
    return true;
}

bool writeConfigFile()
{
    Serial.println(F("Saving config file"));
    DynamicJsonDocument json(1024);
    File file = FileFS.open(CONFIG_FILE, "w");
    if (!file)
    {
        Serial.println(F("Failed to open config file for writing"));
        return false;
    }
    serializeJsonPretty(json, Serial);
    // Write data to file and close it
    serializeJson(json, file);
    file.close();
    Serial.println(F("\nConfig file was successfully saved"));
    return true;
}

void setup_wifi()
{
    Serial.print(F("\nStarting Async_ConfigOnSwichFS using "));
    Serial.print(FS_Name);
    Serial.print(F(" on "));
    Serial.println(ARDUINO_BOARD);
    Serial.println(ESP_ASYNC_WIFIMANAGER_VERSION);

    // Initialize the LED digital pin as an output.
    pinMode(PIN_LED, OUTPUT);

    // Format FileFS if not yet
    if (!FileFS.begin())
    {
        FileFS.format();
        Serial.println(F("SPIFFS/LittleFS failed! Already tried formatting."));
        if (!FileFS.begin())
        {
            // prevents debug info from the library to hide err message.
            delay(100);
            Serial.println(F("LittleFS failed!. Please use SPIFFS or EEPROM. Stay forever"));
            while (true)
            {
                delay(1);
            }
        }
    }

    initAPIPConfigStruct(WM_AP_IPconfig);
    initSTAIPConfigStruct(WM_STA_IPconfig);

    if (!readConfigFile())
    {
        Serial.println(F("Failed to read ConfigFile, using default values"));
    }

    unsigned long startedAt = millis();
    // ESPAsync_WiFiManager ESPAsync_wifiManager(&webServer, &dnsServer, "ConfigOnSwitchFS");
    ESPAsync_wifiManager.setDebugOutput(true);
    ESPAsync_wifiManager.setMinimumSignalQuality(-1);
    // Set config portal channel, default = 1. Use 0 => random channel from 1-13
    ESPAsync_wifiManager.setConfigPortalChannel(0);
    // We can't use WiFi.SSID() in ESP32 as it's only valid after connected.
    // SSID and Password stored in ESP32 wifi_ap_record_t and wifi_config_t are also cleared in reboot
    // Have to create a new function to store in EEPROM/SPIFFS for this purpose
    Router_SSID = ESPAsync_wifiManager.WiFi_SSID();
    Router_Pass = ESPAsync_wifiManager.WiFi_Pass();
    // Remove this line if you do not want to see WiFi password printed
    Serial.println("ESP Self-Stored: SSID = " + Router_SSID + ", Pass = " + Router_Pass);
    ssid.toUpperCase();
    bool configDataLoaded = false;
    // From v1.1.0, Don't permit NULL password
    if ((Router_SSID != "") && (Router_Pass != ""))
    {
        LOGERROR3(F("* Add SSID = "), Router_SSID, F(", PW = "), Router_Pass);
        wifiMulti.addAP(Router_SSID.c_str(), Router_Pass.c_str());
        ESPAsync_wifiManager.setConfigPortalTimeout(120); // If no access point name has been previously entered disable timeout.
        Serial.println(F("Got ESP Self-Stored Credentials. Timeout 120s for Config Portal"));
    }

    if (loadConfigData())
    {
        configDataLoaded = true;
        ESPAsync_wifiManager.setConfigPortalTimeout(120); // If no access point name has been previously entered disable timeout.
        Serial.println(F("Got stored Credentials. Timeout 120s for Config Portal"));
    }
    else
    {
        // Enter CP only if no stored SSID on flash and file
        Serial.println(F("Open Config Portal without Timeout: No stored Credentials."));
        initialConfig = true;
    }

    if (initialConfig)
    {
        Serial.print(F("Starting configuration portal @ "));
        Serial.print(F("192.168.4.1"));
        Serial.print(F(", SSID = "));
        Serial.print(ssid);
        digitalWrite(LED_BUILTIN, LED_ON); // Turn led on as we are in configuration mode.
        // Starts an access point
        if (!ESPAsync_wifiManager.startConfigPortal((const char *)ssid.c_str()))
            Serial.println(F("Not connected to WiFi but continuing anyway."));
        else
        {
            Serial.println(F("WiFi connected...yeey :)"));
        }
        // Stored  for later usage, from v1.1.0, but clear first
        memset(&WM_config, 0, sizeof(WM_config));
        for (uint8_t i = 0; i < NUM_WIFI_CREDENTIALS; i++)
        {
            String tempSSID = ESPAsync_wifiManager.getSSID(i);
            String tempPW = ESPAsync_wifiManager.getPW(i);

            if (strlen(tempSSID.c_str()) < sizeof(WM_config.WiFi_Creds[i].wifi_ssid) - 1)
                strcpy(WM_config.WiFi_Creds[i].wifi_ssid, tempSSID.c_str());
            else
                strncpy(WM_config.WiFi_Creds[i].wifi_ssid, tempSSID.c_str(), sizeof(WM_config.WiFi_Creds[i].wifi_ssid) - 1);

            if (strlen(tempPW.c_str()) < sizeof(WM_config.WiFi_Creds[i].wifi_pw) - 1)
                strcpy(WM_config.WiFi_Creds[i].wifi_pw, tempPW.c_str());
            else
                strncpy(WM_config.WiFi_Creds[i].wifi_pw, tempPW.c_str(), sizeof(WM_config.WiFi_Creds[i].wifi_pw) - 1);

            // Don't permit NULL SSID and password len < MIN_AP_PASSWORD_SIZE (8)
            if ((String(WM_config.WiFi_Creds[i].wifi_ssid) != "") && (strlen(WM_config.WiFi_Creds[i].wifi_pw) >= MIN_AP_PASSWORD_SIZE))
            {
                LOGERROR3(F("* Add SSID = "), WM_config.WiFi_Creds[i].wifi_ssid, F(", PW = "), WM_config.WiFi_Creds[i].wifi_pw);
                wifiMulti.addAP(WM_config.WiFi_Creds[i].wifi_ssid, WM_config.WiFi_Creds[i].wifi_pw);
            }
        }
        ESPAsync_wifiManager.getSTAStaticIPConfig(WM_STA_IPconfig);
        saveConfigData();
    }
    digitalWrite(LED_BUILTIN, LED_OFF); // Turn led off as we are not in configuration mode.
    startedAt = millis();
    if (!initialConfig)
    {
        // Load stored data, the addAP ready for MultiWiFi reconnection
        if (!configDataLoaded)
        {
            loadConfigData();
        }
        for (uint8_t i = 0; i < NUM_WIFI_CREDENTIALS; i++)
        {
            // Don't permit NULL SSID and password len < MIN_AP_PASSWORD_SIZE (8)
            if ((String(WM_config.WiFi_Creds[i].wifi_ssid) != "") && (strlen(WM_config.WiFi_Creds[i].wifi_pw) >= MIN_AP_PASSWORD_SIZE))
            {
                LOGERROR3(F("* Add SSID = "), WM_config.WiFi_Creds[i].wifi_ssid, F(", PW = "), WM_config.WiFi_Creds[i].wifi_pw);
                wifiMulti.addAP(WM_config.WiFi_Creds[i].wifi_ssid, WM_config.WiFi_Creds[i].wifi_pw);
            }
        }
        if (WiFi.status() != WL_CONNECTED)
        {
            Serial.println(F("ConnectMultiWiFi in setup"));
            connectMultiWiFi();
        }
    }

    Serial.print(F("After waiting "));
    Serial.print((float)(millis() - startedAt) / 1000);
    Serial.print(F(" secs more in setup(), connection result is "));

    if (WiFi.status() == WL_CONNECTED)
    {
        Serial.print(F("connected. Local IP: "));
        Serial.println(WiFi.localIP());
    }
    else
    {
        Serial.println(ESPAsync_wifiManager.getStatus(WiFi.status()));
    }
}