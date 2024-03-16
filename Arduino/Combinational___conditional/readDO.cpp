#include "readDO.h"
#include <Arduino.h>

//Single point calibration needs CAL1_V and CAL1_T to be filled
//Two-point calibration needs CAL2_V and CAL2_T to be filled
int16_t CAL1_V = 1870; //mv
int16_t CAL1_T = 243; // 0.1 degrees C
int16_t CAL2_V = 1300; //mv
int16_t CAL2_T = 150; // 0.1 degrees C

//Single-point calibration Mode=0
//Two-point calibration Mode=1
uint8_t TWO_POINT_CALIBRATION = 0;

const uint16_t DO_Table[41] = {
    14460, 14220, 13820, 13440, 13090, 12740, 12420, 12110, 11810, 11530,
    11260, 11010, 10770, 10530, 10300, 10080, 9860, 9660, 9460, 9270,
    9080, 8900, 8730, 8570, 8410, 8250, 8110, 7960, 7820, 7690,
    7560, 7430, 7300, 7180, 7070, 6950, 6840, 6730, 6630, 6530, 6410};

int16_t readDO(uint16_t voltage_mv, uint16_t temperature_c) {
  uint8_t tableIndex = temperature_c / 10;
  if (TWO_POINT_CALIBRATION == 0) {
    uint16_t V_saturation = ((int16_t)temperature_c - CAL1_T) * 7 / 2 + CAL1_V;
    uint16_t result = (uint32_t)voltage_mv * DO_Table[tableIndex] / V_saturation;
    return result;
  }
  else {
    uint16_t V_saturation = ((int16_t)temperature_c - CAL2_T) * (CAL1_V - CAL2_V) / (CAL1_T - CAL2_T) + CAL2_V;
    uint16_t result = (uint32_t)voltage_mv * DO_Table[tableIndex] / V_saturation;
    return result;
  }
}
