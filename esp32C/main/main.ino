#include  "include.h"
Motor motor1 = {motor_in1, motor_in2};
Motor motor2 = {motor_in3, motor_in4};


Encoder encoder1 = {encoder_1, 0};
Encoder encoder2 = {encoder_2, 0};


ServoMotor Servo_0 = {myservo, servoPin};
AsyncUDP udp;


const int IRled = D5;
bool IRled_State = 0;
//---Setup---


void setupMotorsAndEncoders() {
    pinMode(motor1.in1, OUTPUT); pinMode(motor1.in2, OUTPUT);
    pinMode(motor2.in1, OUTPUT); pinMode(motor2.in2, OUTPUT);
    pinMode(encoder1.pin, INPUT); attachInterrupt(digitalPinToInterrupt(encoder1.pin), []{ encoder1.count++; }, RISING);
    pinMode(encoder2.pin, INPUT); attachInterrupt(digitalPinToInterrupt(encoder2.pin), []{ encoder2.count++; }, RISING);

}
//192.168.8.218

void setupServo() {
    ESP32PWM::allocateTimer(0); ESP32PWM::allocateTimer(1);
    ESP32PWM::allocateTimer(2); ESP32PWM::allocateTimer(3);
    Servo_0.attach();
}

void setupwifi()
{
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid,password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  Serial.println(WiFi.localIP());

}
//Setup Light

//---------------------------

void stopWheels()
{
  analogWrite(motor1.in1, 0); 
  analogWrite(motor1.in2, 0);
  analogWrite(motor2.in1, 0); 
  analogWrite(motor2.in2, 0); 
}





//----------------------------



        // self.FORWARD  = "FORWARD"
        // self.BACKWORD = "BACKWARD"
        // self.LEFT     = "LEFT"
        // self.RIGHT    = "RIGHT"
        // self.LEDOFF   = "LEDOFF"
        // self.LEDON   =  "LEDON"




  void wifiEvents()
  {
    if(udp.listen(localUdpPort)) { 
      Serial.println("UDP Listening on port 5555");
      udp.onPacket([](AsyncUDPPacket packet) {
              Serial.write(packet.data(), packet.length());
              Serial.println();
              packet.printf("Got %u bytes of data", packet.length());

              String message = String((char*)packet.data());
              message.trim(); 
        
              if(message == "FORWARD") {

                Serial.println("RECEIVE FORWARD");
                forwardFunc();

              }
              else if(message == "LED0") {
                Serial.println("lightoff.");
                ledOffFunc();
              }
              else if(message == "LED1") {
                Serial.println("lighton.");
                ledOnFunc();
            
              }
              else if(message == "1"){
                Serial.println("shot water.");
                shotwaterFunc();
            
              }
              else if(message == "LEFT") {
                
                Serial.println("left.");
                leftFunc();
              
              }
              else if(message == "RIGHT") {
                
                Serial.println("RIGHT");
                rightFunc();

              }
          
              else {
                Serial.println("Received unknown command.");
              }
              

            

      });
    }




  }



//---------------------------




//-------------------------
void setup() {
  // put your setup code here, to run once:
    setupMotorsAndEncoders();
    setupServo();
    pinMode(IRled,OUTPUT);
    Serial.begin(9600);
    setupwifi();
    wifiEvents();

}


void loop() {


}




void forwardFunc(){

    // encoder1.count = 0; 
    // encoder2.count = 0; 

  // Right Forwar
     analogWrite(motor1.in1, 0); 
     analogWrite(motor1.in2, 255); 
    //  delay(100); 
      delay(100);
      stopWheels();
      delay(400); 
      analogWrite(motor2.in1, 255);
      analogWrite(motor2.in2, 0); 

      // while(encoder2.count < targetSteps) {
      //   Serial.println(encoder2.count);
      
      // }
      delay(100); 
      stopWheels();

}


// void backwardFunc(){



// }

void leftFunc(){
    encoder1.count = 0; 
    encoder2.count = 0; 
    analogWrite(motor1.in1, 0); 
    analogWrite(motor1.in2, 255); 
    analogWrite(motor2.in1, 0);
    analogWrite(motor2.in2, 255); 
    delay(200);
    stopWheels();

}


void rightFunc(){
    encoder1.count = 0; 
    encoder2.count = 0; 
    analogWrite(motor1.in1, 255); 
    analogWrite(motor1.in2, 0);

    analogWrite(motor2.in1, 255);
    analogWrite(motor2.in2, 0); 
      delay(200);
    stopWheels();

  
}


 void ledOffFunc()
 {
  delay(2);
  if(IRled_State == 1)
  {
    digitalWrite(IRled,LOW);
    IRled_State = 0;
  }
  else
  {

  }
  delay(2);
 }


void ledOnFunc(){
   delay(2);
  if(IRled_State == 0)
  {
    digitalWrite(IRled,HIGH);
    IRled_State = 1;
  }
  else
  {

  }
   delay(2);

}


void shotwaterFunc(){
  delay(2);
  for (int pos = 0; pos <= 180; pos += 1) { 
		Servo_0.write(pos);    
		delay(1);   
    Serial.print("a");          
	}
	for (int pos = 180; pos >= 0; pos -= 1) { 
		Servo_0.write(pos);    
		delay(1);            
    Serial.print("b");          
	}
  delay(2);
}



