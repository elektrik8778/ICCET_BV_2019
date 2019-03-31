#define led 13
char data;          // хранит текущий входящий символ
int rul = 320;            //управляющий сигнал от raspberry
String inString = "";    // string to hold input
String label;
boolean b = 0;
boolean a = 0;
int v1 = 0;
int v2 = 0;
int nodrive = 0;
int pedistrain = 0;
int nothing = 0;
#define ENA 9
#define in1 2        //правый мотор
#define in2 3
#define ENB 6        //левый мотор
#define in3 5
#define in4 4

//unsigned int sped = 0;


void setup() {
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
  analogWrite(ENA, v1);
  analogWrite(ENB, v2);

  Serial.begin(9600);             // инициализация последовательного соединения на скорости 9600 бод

  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
}

void loop() {
  // Вывод только при получении данных

  while (Serial.available() > 0) {
    inString = Serial.readStringUntil('\n');
    if (!inString.equals("")) {
      //Serial.print("Value:");
      inString.trim();
      label = inString.substring(0, 3);
      inString = inString.substring(3, inString.length());
      rul = inString.toInt();
      Serial.println(inString);
      // clear the string for new input:
      inString = "";
      if (label.equals("222")) {  // line
        if (rul == 300) {
          stopp();
          delay(500);
        }
        else {
          if (rul < 50) {
            rul = 50;
            b = 1;
            v2 = 100;
            v1 = 130;
          } 
          else {
            b = 0;
            v2 = map(rul, 50, 110, 50, 120);
            v1 = map(rul, 50, 110, 120, 50);
          }
          if (rul > 110) {
            rul = 110;
            a = 1;
            v2 = 130;
            v1 = 100;
          } 
          else {
            a = 0;
            v2 = map(rul, 50, 110, 50, 120);
            v1 = map(rul, 50, 110, 120, 50);
          }
        }
      }
      if (label.equals("111")) {
        if (rul == 1) {
          nodrive ++;
        } 
        else if (rul == 2) {
          pedistrain ++;
        } 
        else if (rul == 3) {
          nothing ++;
          nodrive = 0;
          pedistrain = 0;
        }

        if (nothing >= 2) {
          if (nodrive >= 1) {
            stopp();
            delay(500);
            right();
            delay(1500);
            nodrive = 0;
            pedistrain = 0;
            nothing = 0;
          } 
          else if (pedistrain >= 1) {
            stopp();
            delay(5000);
            nodrive = 0;
            pedistrain = 0;
            nothing = 0;
          }
        }
      }
    }

  }

  Run(v1, v2, a, b);
}

void Run(int x, int y, boolean a, boolean b) {
  digitalWrite(led, HIGH);
  if (a == 0){
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
  } 
  else {
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
  }
  if (b == 0) {
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
  } 
  else {
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
  }

  analogWrite(ENA, x);
  analogWrite(ENB, y+25);


  //  Serial.println("run");
}

void stopp() {
  digitalWrite(led, LOW);
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
  Serial.println("stop");
}

void right(){
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);

  analogWrite(ENA, 150);
  analogWrite(ENB, 150);
}

