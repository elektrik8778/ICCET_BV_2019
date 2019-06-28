#define delitel A0
float znah ;
void setup()
{
  pinMode(A0 , INPUT);
  Serial.begin(9600);

}

void loop()
{
  znah = analogRead(delitel);
  Serial.println(map(znah, 0, 1024, 0, 8));
  delay(100);
}

float map(float val, float in_min, float in_max,  float out_min, float out_max) {
  return (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
