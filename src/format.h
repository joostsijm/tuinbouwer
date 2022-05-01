#ifndef FORMAT_H
#define FORMAT_H
#include <Arduino.h>
#include <ArduinoJson.h>

String format_cycle_time(int time_climate_cycle, int cycle_time, int time_ventilator_control, int ventilator_percentage, int time_heater_control, int heater_percentage);
String format_climate_cycle(int cycle_time, String ventilator_percentage, int heater_percentage);
String format_climate(int16_t temperature, int16_t humidity);
String format_controls(int power_heating, int power_lighting, int power_dehumidifier, int power_ventilation);
String format_status(String formatted_tme, int16_t temperature, int16_t humidity,int power_heating, int power_lighting, int power_dehumidifier, int power_ventilation, int cycle_time, int ventilator_percentage, int heater_percentage);
String format_sensor_data_json(int16_t space_id, int16_t temperature, int16_t humidity);

#endif