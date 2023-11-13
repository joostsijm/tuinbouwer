#include "wifi.h"

String format_cycle_time(int time_climate_cycle, int cycle_time, int time_ventilator_control, int ventilator_percentage, int time_heater_control, int heater_percentage)
{
    unsigned long currentMillis = millis();
    return F("seconds: ") + String(currentMillis / 1000) + F("s") + F(" climate: ") + String((time_climate_cycle - currentMillis) / 1000) + F("/") + String(cycle_time / 1000) + F("s ") + F(" ventilator: ") + String((time_ventilator_control - currentMillis) / 1000) + F("/") + String((cycle_time / 100 * ventilator_percentage) / 1000) + F("s ") + F(" heating: ") + String((time_heater_control - currentMillis) / 1000) + F("/") + String((cycle_time / 100 * heater_percentage) / 1000) + F("s");
}

String format_climate_cycle(int cycle_time, int ventilator_percentage, int heater_percentage)
{
    return F("cycle: ") + String(cycle_time / 1000) + F("s") + F(" ventilator: ") + String(ventilator_percentage) + F("%") + F(" heater: ") + String(heater_percentage) + F("%");
}

String format_climate(int16_t temperature, int16_t humidity)
{
    String climate_str = F("Temperature: ");
    if (temperature == ~0)
    {
        climate_str = climate_str + F("Error");
    }
    else
    {
        climate_str = climate_str + String(temperature / 10) + F(".") + String(temperature % 10) + F(" *C");
    }
    climate_str = climate_str + F(" Humidity: ");
    if (humidity == ~0)
    {
        climate_str = climate_str + F("Error");
    }
    else
    {
        climate_str = climate_str + String(humidity / 10) + F(".") + String(humidity % 10) + F(" %");
    }
    return climate_str;
}

String format_controls(int power_heating, int power_lighting, int power_dehumidifier, int power_ventilation)
{
    return F("Heating: ") + String(power_heating) + F(" Lighting: ") + String(power_lighting) + F(" Dehumidifier: ") + power_dehumidifier + F(" Ventilation: ") + power_ventilation;
}

String format_status(String formatted_tme, int16_t temperature, int16_t humidity, int power_heating, int power_lighting, int power_dehumidifier, int power_ventilation, int cycle_time, int ventilator_percentage, int heater_percentage)
{
    return formatted_tme + F(" ") + format_climate(temperature, humidity) + F(" ") + format_controls(power_heating, power_lighting, power_dehumidifier, power_ventilation) + F(" ") + format_climate_cycle(cycle_time, ventilator_percentage, heater_percentage);
}

String format_sensor_data_json(int16_t space_id, int16_t temperature, int16_t humidity)
{
    StaticJsonDocument<200> json_document;
    json_document[F("space_id")] = space_id;
    json_document[F("temperature")] = String(temperature / 10) + F(".") + String(temperature % 10);
    json_document[F("humidity")] = String(humidity / 10) + F(".") + String(humidity % 10);
    json_document[F("power")] = F("0");

    String json_string;
    serializeJson(json_document, json_string);
    return json_string;
}
