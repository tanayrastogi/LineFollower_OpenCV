const double MICRO_PER_SEC = 1000000.0; // Time conversion 
const double ROBOT_BASE = 0.21/2; // Distance from the center of the car to the wheel (L/2)
const float pi = 3.1415926535897932384626433832795;
const double WHEEL_RADIUS = 0.06425/2;

//Motor Class with different paramters for configuring the connections
class Motor {
private:
  bool INVERSE; // Left/right wheel (CW or CCW rotation)
  double Kp, Ki, Kd; // PID gains
  unsigned long time_prev, time_now = 0; // Sampling times
  double angular_vel = 0; // Current angular velocity of wheel
  double time_diff; // Sampling period 
  double now_err = 0, prev_err = 0, integ_err = 0, diff_err = 0; // PID errors
  double TICS_PER_ROTATION = 384; // This can be varied based on interrupt configuration
  int current_pwm = 0; // PWM value
  
public:
  byte ENCODER_PIN, OUT1, OUT2, ENB; // Pin numbers
  unsigned int tic_count; // Tic counter
  Motor(byte enc_pin, byte out1, byte out2, byte enb, bool inverse,
    double Kp, double Ki, double Kd); // Constructor 
  void calc_angular_vel();
  void rotate(double ref, double turn);
  double get_angular_vel();
  void tic_counter();
  void pid_controller(double ref);
};

//Initialize the motor parameters (constructor) 
Motor::Motor(byte enc_pin, byte out1, byte out2, byte enb, bool inverse,
  double Kp, double Kd, double Ki){
  this->ENCODER_PIN = enc_pin;
  this->OUT1 = out1;
  this->OUT2 = out2;
  this->ENB = enb;
  this->INVERSE = inverse;
  this->Kp = Kp;
  this->Kd = Kd;
  this->Ki = Ki;
  this->time_prev = micros();
  pinMode(enc_pin, INPUT_PULLUP);
  pinMode(out1, OUTPUT);
  pinMode(out2, OUTPUT);
  pinMode(enb, OUTPUT);
}

// Function to calculate angular velocity
void Motor::calc_angular_vel(){
  // Calculate time difference (seconds)
  time_now = micros();
  time_diff = (time_now - time_prev)/MICRO_PER_SEC;
  
  // Calcuate angular velocity (degree/s)
  angular_vel = (tic_count/TICS_PER_ROTATION)* 2 * pi/time_diff;
  
  // Store current time value for next loop
  time_prev = time_now;
  
  // Clear tic_counter
  tic_count = 0; 
}
 
// Function to rotate the motor, parameters: reference velocity and direction of motor
void Motor::rotate(double ref, double turn) {
      // Calculate the angular velocity (deg/s) of the wheel
  calc_angular_vel();
  
  // Calcuate the reference angular velocity (straight line condition)
  if (turn == 0) {
    // Calculate PWM value
    pid_controller(ref/WHEEL_RADIUS);
  }
  // Calculate angular velocity of wheel (turning condition)
  else if (INVERSE) {
    pid_controller((ref - turn * ROBOT_BASE)/WHEEL_RADIUS);
  }
  else {
    pid_controller((ref + turn * ROBOT_BASE)/WHEEL_RADIUS);
  }
    
  // Rotation direction of the motor
  if (INVERSE) {
    digitalWrite(OUT1,HIGH);
    digitalWrite(OUT2,LOW); 
  }
  else {
    digitalWrite(OUT1,LOW);
    digitalWrite(OUT2,HIGH); 
  }
    
  // PWM output  for motor
  analogWrite(ENB,current_pwm); 
}

// Control algorithm to maintain the speed
void Motor::pid_controller(double ref){
  // Calculate errors
  now_err = ref - angular_vel;
  integ_err = integ_err + now_err;
  diff_err = (now_err - prev_err)/time_diff;
  
  // Calculate PWM output  for motor
  current_pwm = constrain(Kp * now_err + Ki * integ_err + Kd * diff_err, 0, 255); 
  
  // Store error for next loop
  prev_err = now_err;
}

// Function to read the current angular velocity of motors
double Motor::get_angular_vel(){
  // Return angular velocity
  return angular_vel;
}

// Function to increment the tics for each motor.
void Motor::tic_counter(){
  tic_count++; 
}
