
String potenciometro;
String servomotor;
String v_union;

void setup() {
  
  Serial.begin(9600);
}
void loop() {
  potenciometro = String(analogRead(A0)/1023);
  servomotor = String(analogRead(A1)/1023);
  v_union = potenciometro +'&'+ servomotor;
  
  Serial.println(v_union);
  delay(500);

}
