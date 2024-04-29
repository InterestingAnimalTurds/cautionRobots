//--------------Defining-----------//
Servo myservo; 

int servoPin = D0;


// const int motor_in1 = D4,
//           motor_in2 = D3, 
//           motor_in3 = D2, 
//           motor_in4 = D1;

//For Last One
const int motor_in1 = D3,
          motor_in2 = D4, 
          motor_in3 = D1, 
          motor_in4 = D2;


const int encoder_1 = D8, 
          encoder_2 = D9;


int encoder_1_count = 0, 
    encoder_2_count = 0;



const int targetSteps = 10;
//--------------------------------//