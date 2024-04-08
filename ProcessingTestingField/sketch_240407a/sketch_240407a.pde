import processing.net.*;

Client myClient; 
String inString; 


int circleSizeX = 50;
int circleSizeY = 50;



void setup() {

    size(800, 800);
    background(0);
    myClient = new Client(this, "127.0.0.1", 9911);
}




void draw() {
    background(0);
    ellipse(mouseX, mouseY, circleSizeX, circleSizeY);
    fill(255,255,255,255);
    noStroke();
    if (myClient.available() > 0) { 
    inString = myClient.readString(); 
    println(inString); 
  }

}
