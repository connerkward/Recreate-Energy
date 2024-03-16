#include <DFRobot_PH.h>
#include <EEPROM.h>
#include <OneWire.h>
#include <Arduino.h>
#include <LowPower.h>
#include "getTemp.h"
#include "readDO.h"

#define greenPin 7 // green LED Pin
#define redPin 4 // red LED Pin
int DS18S20_Pin = 2; // temperature pin, DS18S20 Signal pin on digital 2
OneWire ds(DS18S20_Pin); // temperature chip i/o on digital pin 2
#define PH_PIN A1 // pH sensor pin
DFRobot_PH ph;
#define DO_PIN A2 // O2 sensor pin
#define VREF 5000 // VREF (mv)
#define ADC_RES 1024 // ADC Resolution
String command; // commands from Raspberry Pi
float voltage, phValue; // float needed for DFRobot_PH
uint16_t temperature, ADC_Raw, ADC_Voltage, DO_Value; // everything else is uint16

void setup() {
  Serial.begin(9600);
  pinMode(greenPin, OUTPUT);
  pinMode(redPin, OUTPUT);  
  ph.begin();
}

void loop() {
  ADC_Raw = analogRead(DO_PIN);
  ADC_Voltage = (uint32_t)VREF * ADC_Raw / ADC_RES;
  temperature = getTemp(ds); // read temperature sensor to execute temperature compensation
  voltage = analogRead(PH_PIN) / 1024.0 * 5000; // read the voltage
  if (temperature != 0 && ADC_Raw != 0) {
    phValue = ph.readPH(voltage, (float)temperature / 10); // convert voltage to pH with temp compensation
  }
  else {
    phValue = 0;
  }
  if (temperature != 0 && ADC_Raw != 0) {
    DO_Value = readDO(ADC_Voltage, temperature);
  }
  else {
    DO_Value = 0;
  }
//  phValue = ph.readPH(voltage, (float)temperature / 10); // convert voltage to pH with temp compensation
  Serial.print(temperature);
  Serial.print(',');
  Serial.print(phValue);
  Serial.print(',');
  Serial.print((String)ADC_Raw);
  Serial.print(',');
  Serial.print(ADC_Voltage);
  Serial.print(',');
//  Serial.println(readDO(ADC_Voltage, temperature));
  Serial.print(DO_Value);
  ph.calibration(voltage, temperature); // calibration process by serial CMD
  
  if (Serial.available()) {
    command = Serial.readStringUntil('\n');
    command.trim();
    
    if (command.equals("on")) {
      digitalWrite(greenPin, HIGH);
      digitalWrite(redPin, LOW);
    }
    else if (command.equals("off")) {
      digitalWrite(greenPin, LOW);
      digitalWrite(redPin, HIGH);
    }
  }
  
  delay(100); // needed to prevent sleep from eating serial bytes
  for (int i = 0; i < 2; ++i) { // SLEEP_8S sleeps for 2 minutes every 15
    LowPower.idle(SLEEP_1S, ADC_OFF, TIMER2_OFF, TIMER1_OFF, TIMER0_OFF, SPI_OFF, USART0_OFF, TWI_OFF);
  }
}
