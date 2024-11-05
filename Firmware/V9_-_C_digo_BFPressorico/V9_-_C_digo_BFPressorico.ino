// 10.08.2020

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
int media = 0;
int leito = 0;
int ValorEscrito = 0;
int Val = 0;
int comunicando = 0;  //indica que há uma comuniação em andamento
int nivel = 0, i = 0,j = 0;  //variáveis auxiliares de escrita no LCD
int pausa = 0, ValorLido = 0, indice = 0, soma = 0;
// Handle received and sent messages
String message = "";
char incomingChar;
String resistenciaString = "";
unsigned long Time;

int Led_On = 2;
int Led_Com = 4;
int npontos=0, estouro = 0;
float tempo_inicio=0, tempo_fim=0;

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
  leito =0;
  
  if(SerialBT.hasClient()==1 and pausa==0){
    digitalWrite(Led_On,LOW);
    digitalWrite(Led_Com,HIGH);
    lcd.clear();
    lcd.print("Conectando...");
    comunicando=0;
    delay(100);
    }
  
  if(SerialBT.hasClient()==0 and leito == 0){
    digitalWrite(Led_Com,LOW);
    digitalWrite(Led_On,HIGH);
    lcd.clear();
    lcd.print("Aguardando");
    lcd.setCursor(0,1); 
    lcd.print ("Comunica");
    lcd.write(1);
    lcd.write(2);
    lcd.print("o...");
    pausa=0;
    leito=1;
    comunicando=0;
    delay(100);
    }
    
  if(SerialBT.read()=='i' or comunicando==1){   
    //Serial.print("npontos: ");
    //Serial.println(npontos);
    pausa=1;
// 90mV/kPa = 90mV/7.5mmHg
// 4095 ==> 4500mV
    media = analogRead(pot)/15; 
    
    Serial.println(analogRead(pot));
    Serial.println(media);
    nivel = media/17;
    ValorEscrito = media;
    Val=Val+ValorEscrito;
    npontos++;
    if(comunicando == 0){
      tempo_inicio = millis();
      }
    if (npontos%10==0){
      SerialBT.print(Val/10);
      Val=0;
      if (npontos==1){
          
          lcd.clear();
          lcd.setCursor(0,0);
          lcd.print("Press");
          lcd.write(2);
          lcd.print("o:");
          lcd.write(5);
          lcd.write(5);
          lcd.write(5);
          lcd.write(5);
          //lcd.setCursor(12,0);
          //lcd.print("mmHg");}
        }
        for (i=0;i<nivel;i++){
          lcd.setCursor(i,1);
          lcd.write(4);
          delay(3);
         }
        for (j=nivel;j<16;j++){
          lcd.setCursor(j,1);
          lcd.write(5);
          delay(3);
         }
      
      
      }
    if (comunicando == 0){
      tempo_inicio = millis();
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Press");
      lcd.write(2);
      lcd.print("o:");
      lcd.write(5);
      lcd.write(5);
      lcd.write(5);
      lcd.write(5);
      //lcd.setCursor(12,0);
      //lcd.print("mmHg");}
    }
    
   if (ValorEscrito > 1000){
       ValorEscrito = ValorEscrito%1000;
       }
    if (ValorEscrito>=100){ //pressão com três dígitos
      lcd.setCursor(9,0);}
    if (10<ValorEscrito and ValorEscrito<100){ //pressão com dois dígitos
      lcd.setCursor(9,0);
      lcd.write(5);}
    if (ValorEscrito<10 and ValorEscrito>=0){ //pressão com um dígitos
      lcd.setCursor(9,0);
      lcd.write(5);
      lcd.write(5);}
    lcd.print(ValorEscrito);
    
    comunicando=1;
      
    delay(3);
  } 
  if (SerialBT.read()=='p'){
    tempo_fim = millis();
    lcd.clear();        
    lcd.setCursor(3,0); 
    lcd.print("Biofeedback");
    lcd.setCursor(3,1); 
    lcd.print ("Press");
    lcd.write(3);
    lcd.print("rico");
    comunicando=0;
    pausa=1;
    Serial.print("npontos: ");
    Serial.println(npontos);
    Serial.print("Tempo Init: ");
    Serial.println(tempo_inicio);
    Serial.print("Tempo Final: ");
    Serial.println(tempo_fim);
    Serial.print("Tempo Total: ");
    Serial.println(tempo_fim-tempo_inicio);
    delay(20);
  }
}
