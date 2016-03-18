/*
Arduino Hall Effect Sensor Project
by Arvind Sanjeev
Please check out  http://diyhacking.com for the tutorial of this project.
DIY Hacking
*/
 const float pi = 3.1415926;
 volatile byte revs;
 unsigned int rpm;
 unsigned long timeold;

 int r = 10; //in inches
 double car_speed;
 int ipm;
 
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
   if (revs >= 5) {
     rpm = revs/((millis() - timeold)/1000/60);
     timeold = millis();
    
     ipm = rpm*2*pi*r; //inches per minute

     car_speed = ((ipm*60)/12)/5280;
     
     Serial.println(rpm,DEC);
     Serial.println(car_speed, DEC);
     
      revs = 0;
   }
  }
  
 void magnet_detect()//This function is called whenever a magnet/interrupt is detected by the arduino
 {
   revs++;
   Serial.println("detect");
 }
