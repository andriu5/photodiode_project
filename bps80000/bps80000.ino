enum {
 ANALOG_INPUT_PIN = A0,
 UPDATE_INTERVAL_MICROS = 200,
 MODE_2_CONSECUTIVE_READS = 5000,
};
 
unsigned long next_update;
int reads;
int mode;
 
void setup() {
  // Enable pull-ups to avoid floating inputs
  digitalWrite(A0, HIGH);

  // Init serial
  Serial.begin(115200);
  //analogReference(EXTERNAL);
  mode = 0;
}
 
void mode1() {
  int analog_value = analogRead(ANALOG_INPUT_PIN);
  Serial.println(analog_value);
  delay(100);
}
 
void mode2() {
 
unsigned long current_micros;
current_micros = micros();
 
if(current_micros >= next_update) {
  byte b1, b2;
  int analog_value;
  next_update = next_update + UPDATE_INTERVAL_MICROS;
 
  analog_value = analogRead(ANALOG_INPUT_PIN);
  reads--;
  b1 = analog_value&0xFF;
  b2 = ( analog_value >> 8 ) & 0xFF;
  Serial.write(b1);
  Serial.write(b2);
  
  if(reads <= 0) {
    mode = 0;
    Serial.write(0xFF);
    Serial.write(0xFF);
    }
  }
}
 
void loop() {
  
int rcv;
rcv = Serial.read();

if(rcv == '1') {
  mode = 1;
  } else if(rcv == '2') {
    mode = 2;
    reads = MODE_2_CONSECUTIVE_READS;
    next_update = micros();
    } else if(rcv == '0') {
      if(mode == 2) {
        Serial.write(0xFF);
        Serial.write(0xFF);
        }
    }
switch(mode) {
  case 1:
    mode1();
  break;
  case 2:
    mode2();
  break;
  default:
    delay(200);
  break;
}
 
}
