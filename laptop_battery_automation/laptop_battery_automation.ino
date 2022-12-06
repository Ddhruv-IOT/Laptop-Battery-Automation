int D0 = 16;
int D2 = 2;
int D5 = 14;

void setup() {
  Serial.begin(9600);
  Serial.println("Hi");
  pinMode(D0, OUTPUT);
  pinMode(D2, OUTPUT);
  pinMode(D5, OUTPUT);
  digitalWrite(D0, HIGH);
  digitalWrite(D2, HIGH);
  digitalWrite(D5, HIGH);
}

String data;
int incomingByte = 0;
int prevByte = 0;

void loop() {

  while (!Serial.available()) {
    ;
  }

  data = Serial.readString(); // incomingByte = Serial.parseInt();
  incomingByte = data.toInt();
  
  if (incomingByte == 1 and prevByte != incomingByte) {
    digitalWrite(D0, HIGH);
    digitalWrite(D2, LOW);
    digitalWrite(D5, LOW);
    prevByte = incomingByte;
    }

    if (incomingByte == 0 and prevByte != incomingByte) {
    digitalWrite(D2, HIGH);
    digitalWrite(D0, LOW);
    digitalWrite(D5, HIGH);
    prevByte = incomingByte;
    }

  
}
