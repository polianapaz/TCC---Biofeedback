//01/04/2020
// Código com "histerese" de valor +3 e -3 e fazendo a média de 30 valores


#include "BluetoothSerial.h"
#include <LiquidCrystal.h>

// Check if Bluetooth configs are enabled
#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

// Bluetooth Serial object
LiquidCrystal lcd(22,23,5,18,19,21);
BluetoothSerial SerialBT;

// GPIO where LED is connected to
byte c [8]={B00000,B00000,B01110,B10000,B10000,B10001,B01110,B00100};
byte ao[8]={B01110,B00000,B01110,B00001,B01111,B10001,B01111,B00000};
byte oh[8]={B00010,B00100,B00000,B01110,B10001,B10001,B10001,B01110};
byte full[8]={B11111,B11111,B11111,B11111,B11111,B11111,B11111,B11111};
byte white[8]={B00000,B00000,B00000,B00000,B00000,B00000,B00000,B00000};
const int pot =  34;
int ValorFinal =0, ValorEscrito=0,test=0, nivel=0, i=0,j=0,pausa=0, ValorLido=0, indice=0, valor=0;
// Handle received and sent messages
String message = "";
char incomingChar;
String resistenciaString = "";

int Led_On = 2;
int Led_Com = 4;


void setup() {
  pinMode(Led_On, OUTPUT);
  pinMode(Led_Com, OUTPUT);
  digitalWrite(Led_On,HIGH);
  // LCD Inicialização
  lcd.begin(16, 2);
  lcd.createChar(1, c);
  lcd.createChar(2, ao);
  lcd.createChar(3, oh); 
  lcd.createChar(4, full); 
  lcd.createChar(5, white); 
  lcd.clear();
  lcd.setCursor(3,0); 
  lcd.print("Biofeedback");
  lcd.setCursor(3,1); 
  lcd.print ("Press");
  lcd.write(3);
  lcd.print("rico");
  delay(2000);
  lcd.clear();
  lcd.print("Aguardando");
  lcd.setCursor(0,1); 
  lcd.print ("Comunica");
  lcd.write(1);
  lcd.write(2);
  lcd.print("o...");
  Serial.begin(115200);
  // Bluetooth device name
  SerialBT.begin("Biofeedback");
  delay(500);
}

void loop() {
 Serial.println(pausa);
  if(SerialBT.hasClient()==1 and pausa==0){
    digitalWrite(Led_Com,HIGH);
    lcd.clear();
    lcd.print("Conectando...");
    test=0;
    delay(100);
    }
  if(SerialBT.hasClient()==0){
    digitalWrite(Led_Com,LOW);
    lcd.clear();
    lcd.print("Aguardando");
    lcd.setCursor(0,1); 
    lcd.print ("Comunica");
    lcd.write(1);
    lcd.write(2);
    lcd.print("o...");
    pausa=0;
    test=0;
    delay(100);
    }
  if(SerialBT.read()=='i' or test==1){   

    pausa=1;

    for (int i=0; i<=29; i++){
      ValorLido = analogRead(pot)/4;    
      if (ValorLido>=720){
        ValorLido=720;}
      Serial.print("valor=");
      Serial.println(valor);
      valor=valor+ValorLido;}
      
    ValorFinal=valor/30;
    valor=0;
    /*Serial.print("Valor Lido=");
    Serial.println(ValorLido);
    Serial.print("valor=");
    Serial.println(valor);
    Serial.print("Valor Final=");
    Serial.println(ValorFinal);*/
    nivel=ValorFinal/45;

   if (indice==0){
      indice=1;
      ValorEscrito=ValorFinal;}
   if (abs(ValorFinal-ValorEscrito)>=3){
      ValorEscrito=ValorLido;}

    SerialBT.print(ValorEscrito);
    lcd.setCursor(0,0);
    lcd.print("Press");
    lcd.write(2);
    lcd.print("o: ");
    lcd.print(ValorEscrito);
    lcd.print("mmHg");
    if (ValorEscrito<100){
      lcd.setCursor(11,0);
      lcd.print("mmHg");
      lcd.write(5);
      if (ValorEscrito<10){
        lcd.setCursor(10,0);
        lcd.print("mmHg");
        lcd.write(5);
        }
      }
    for (i=0;i<nivel;i++){
      lcd.setCursor(i,1);
      lcd.write(4);
      delay(10);
      }
    for (j=nivel;j<=16;j++){
      lcd.setCursor(j,1);
      lcd.write(5);
      delay(10);
      }
    test=1;  
    delay(150);
  } 
    if (SerialBT.read()=='p'){
    lcd.clear();
    lcd.print("PAUSA");
    test=0;
    pausa=1;
    delay(20);
  } /*
  ValorLido = analogRead(pot)/2;    
  SerialBT.print(ValorLido);
  Serial.println(ValorLido); 
  delay(50); */
}
