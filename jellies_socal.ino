#define LED_PIN A5
#define LED_PIN2 A4
#define LED_PIN3 A3
#define LED_PIN4 9
#define LED_PIN5 7
#define BUTTON_PIN 13
#define LED_TIME 1
int JELLY_PIN1_U = 5;
int JELLY_PIN1_D = 6;
int JELLY_PWR1 = 4;
int JELLY_SPEED_1;
int JELLY_SPEED_2;
int JELLY_PIN2_U = 10;
int JELLY_PIN2_D = 11;
int JELLY_PWR2 = 12;

void setup() {
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
  pinMode(LED_PIN2, OUTPUT);
  pinMode(LED_PIN3, OUTPUT);
  pinMode(LED_PIN4, OUTPUT);
  pinMode(LED_PIN5, OUTPUT);
  pinMode(BUTTON_PIN, INPUT);
  pinMode(JELLY_PIN1_U, OUTPUT);
  pinMode(JELLY_PIN1_D, OUTPUT);
  pinMode(JELLY_PWR1, OUTPUT);
  pinMode(JELLY_PIN2_U, OUTPUT);
  pinMode(JELLY_PIN2_D, OUTPUT);
  pinMode(JELLY_PWR2, OUTPUT);
  
}
void loop() {

  
  // Use the potentiometer readings to set a speed between 0 and 255
  JELLY_SPEED_1 = (analogRead(A0));
  JELLY_SPEED_2 = (analogRead(A1));

  // Set the power on
  digitalWrite(JELLY_PWR1,HIGH);
  digitalWrite(JELLY_PWR2,HIGH);
  
  // LED CONTROL

  // Light up LED for Jelly 1 fast speeds
  //Jelly control speeds
  
  if (analogRead(A0) > 500) {
    digitalWrite(LED_PIN2, HIGH);
    digitalWrite(LED_PIN3, LOW);
    analogWrite(JELLY_PIN1_U,255);
    analogWrite(JELLY_PIN1_D,0);
    delay(4000);
    analogWrite(JELLY_PIN1_D,255);
    analogWrite(JELLY_PIN1_U,0);
    delay(4000);
  }
  // Light up LED for Jelly 1 slow speeds
  else{
    digitalWrite(LED_PIN2, LOW);
    digitalWrite(LED_PIN3, HIGH);
    analogWrite(JELLY_PIN1_U,135);
    analogWrite(JELLY_PIN1_D,0);
    delay(4000);
    analogWrite(JELLY_PIN1_D,135);
    analogWrite(JELLY_PIN1_U,0);
  }
  // Light up LED for Jelly 2 fast speeds
  if (analogRead(A1) > 500) {
    digitalWrite(LED_PIN4, HIGH);
    digitalWrite(LED_PIN5, LOW);
    analogWrite(JELLY_PIN2_U,255);
    analogWrite(JELLY_PIN2_D,0);
    delay(4000);
    analogWrite(JELLY_PIN2_D,255);
    analogWrite(JELLY_PIN2_U,0);
  }
  // Light up LED for Jelly 2 slow speeds
  else{
    digitalWrite(LED_PIN4, LOW);
    digitalWrite(LED_PIN5, HIGH);
    analogWrite(JELLY_PIN2_U,175);
    analogWrite(JELLY_PIN2_D,0);
    delay(4000);
    analogWrite(JELLY_PIN2_D,175);
    analogWrite(JELLY_PIN2_U,0);
  }
  // Pause jellies for 10 seconds
  if (digitalRead(BUTTON_PIN) == LOW) {
    digitalWrite(LED_PIN, HIGH);
    analogWrite(JELLY_PIN1_U,0);
    analogWrite(JELLY_PIN1_D,0);
    delay(LED_TIME*1000);
  }
  else {
    digitalWrite(LED_PIN, LOW);
  }
 
  
}
