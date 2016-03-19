/*
 * attaches an interrupt that is triggered with each rotation of the tire. 
 * calculates speed and rpms assuming a tire with diameter of 20 inches. 
 */
 const float pi = 3.1415926;
 int revs;
 double rpm;
 double timeold;
 double r = 10; //in inches
 double car_speed;
 double ipm;
 double curtime;
 double ms;
 double minutes;
 
  void setup()
 {
   Serial.begin(9600);
   attachInterrupt(0, magnet_detect, RISING);//Initialize the intterrupt pin (Arduino digital pin 2)
   revs = 0;
   rpm = 0;
   timeold = 0;
 }
 
 void loop()//Measure RPM
 {
   if (revs >= 2) {
     curtime = millis();
     ms = curtime - timeold;
     minutes = ms/1000/60;
     rpm = revs/minutes;
     timeold = millis();
     ipm = rpm*2.0*pi*r; //inches per minute
     car_speed = ((ipm*60)/12)/5280;

     Serial.printf("%d,%d", rpm, car_speed);
     
     revs = 0;
   }
  }
  
 void magnet_detect()//This function is called whenever a magnet/interrupt is detected by the arduino
 {
   revs++;
 }
