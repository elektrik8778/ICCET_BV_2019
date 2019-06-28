#define led 13
char data;          // хранит текущий входящий символ
int rul = 320;            //управляющий сигнал от raspberry
String inString = "";    // string to hold input
boolean b = 0;
boolean a = 0;
int v1 = 0;
int v2 = 0;
#define ENA 9
#define in1 5        //правый мотор
#define in2 4
#define ENB 6        //левый мотор
#define in3 3
#define in4 2

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
      rul = inString.toInt();
      Serial.println(inString);
      // clear the string for new input:
      inString = "";
      
      if (rul < 50){
        rul = 50;
        b = 1;
        v2 = 100;
        v1 = map(rul, 50, 110, 150, 50);
      } else {
        b = 0;
        v2 = map(rul, 50, 110, 50, 150);
        v1 = map(rul, 50, 110, 150, 50);
      }
      if (rul > 110){
        rul = 110;
        a = 1;
        v2 = map(rul, 50, 110, 50, 150);
        v1 = 100;
      } else {
        a = 0;
        v2 = map(rul, 50, 110, 50, 150);
        v1 = map(rul, 50, 110, 150, 50);
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
  } else {
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
  }
  if (b == 0) {
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
  } else {
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
