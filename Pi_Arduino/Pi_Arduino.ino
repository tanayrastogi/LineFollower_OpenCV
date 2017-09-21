#include "motors.h"
//#include "raspberryCom.ino"

// Robot parameters
//const double WHEEL_RADIUS = 0.06425/2;

unsigned int left_enc_count, right_enc_count; // Encoder counts?
unsigned long time_prev, time_now;
double linear_vel = 0;
double angular_vel = 0;
bool newData = false;
unsigned int count_noData = 0;
unsigned int threshold_noData = 10;

// Create motor objects with connections and  parameters
// Arguements: encoder pin, to motor : out1,out2,enable pin,inverse direction,Kp,Ki,Kd
Motor left_motor(3, 10, 11, 6, true, 69.5, 0.31, 0.00045);
Motor right_motor(2, 8, 9, 5, false, 69.5, 0.31, 0.00045);

void setup() {
  // Serial communication initialization
  Serial.begin(9600);

  // Configure interrupt pins for encoders (calls tick_counter on interrupt)
  attachInterrupt(digitalPinToInterrupt(left_motor.ENCODER_PIN), left_tic_counter , CHANGE);
  attachInterrupt(digitalPinToInterrupt(right_motor.ENCODER_PIN), right_tic_counter , CHANGE);
}

void loop() {
  // Function to read and intrepret the serial data received from raspberrypi
  newData = readSerialCmd(linear_vel, angular_vel);

  if (!newData) {
    count_noData++;
  }
  else {
    count_noData = 0;
  }

  if (count_noData > threshold_noData) {
    linear_vel = 0;
    angular_vel = 0;
  }

  // Move Robot - Use below functions to set reference speed and direction of motor.
  left_motor.rotate(linear_vel, angular_vel);
  right_motor.rotate(linear_vel, angular_vel);

  //Serial communication
//  Serial.print("\nSignal Input\n");
//  Serial.print(linear_vel);
//  Serial.print("\t");
//  Serial.println(angular_vel);
//  Serial.print("Wheel velocity\n");
//  Serial.print(left_motor.get_angular_vel());
//  Serial.print("\t");
//  Serial.println(right_motor.get_angular_vel());

  // Defines control loop frequency
  delay(50);
}

// Callback functions when interrupt are triggered by encoders
void left_tic_counter() {
  // Call motor tick counter
  left_motor.tic_counter();
}

void right_tic_counter() {
  // Call motor tick counter
  right_motor.tic_counter();
}

