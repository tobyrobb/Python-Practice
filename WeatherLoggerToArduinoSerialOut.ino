// A simple serial publisher of weather sensor data

// T robb 1 sep 12
// modded 31 oct 13
//modded 27 dec 14

#include <SPI.h>

#include <dht11.h>
#include <Wire.h>
#include <Adafruit_BMP085.h>
 
dht11 DHT11;

Adafruit_BMP085 bmp;
  
// define some variables

float temp_outdoor;
float humidity_outdoor;
float pressure_outdoor;
float rainTrigger;
float temp_indoor;
float light_indoor;

//define some hardware pins
#define raintriggerPin A0
#define rainPin A1
#define ldrPin A2
#define DHT11PIN A3

void setup()
{ 
  Serial.begin(9600);
  bmp.begin(); 
}

void loop()
{
  dhllRead();  // must read values from the sensor

//output serial data
// leading with a comma, who knows why, just cause corresponding python code
// is expecting it

 Serial.print(",");
 Serial.print((bmp.readPressure()/100));
 Serial.print(",");
 Serial.print(bmp.readTemperature());
 Serial.print(",");
 Serial.print((float)DHT11.humidity, 2);
 Serial.print(",");
 Serial.print(dewPointFast(bmp.readTemperature(), DHT11.humidity));
 Serial.print(",");
 Serial.println(analogRead(ldrPin));
 
//   FUNCTIONS
    
}

// Read humidity sensor
void dhllRead()
 {
   
  int chk = DHT11.read(DHT11PIN);
 
 }

// delta max = 0.6544 wrt dewPoint()
 // 5x faster than dewPoint()
 // reference: http://en.wikipedia.org/wiki/Dew_point
 double dewPointFast(double celsius, double humidity)
 {
         double a = 17.271;
         double b = 237.7;
         double temp = (a * celsius) / (b + celsius) + log(humidity/100);
         double Td = (b * temp) / (a - temp);
         return Td;
 }
 
