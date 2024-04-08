

//------------
struct ServoMotor {
    Servo servo;
    int pin;
    void attach(int minMicroseconds = 1000, int maxMicroseconds = 2000) {
        servo.setPeriodHertz(50); 
        servo.attach(pin, minMicroseconds, maxMicroseconds);
    }
    void write(int position) {
        servo.write(position);
    }
};
//------------