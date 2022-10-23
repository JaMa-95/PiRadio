#include <RotaryEncoder.h>
#include <Arduino.h>

// 7. Buttons
// 2. Rotary Encoder
// 1. absolut encoder -> Lautstärke
// string with all infos
uint8_t buttonOnOff = 4;
uint8_t buttonLang = 14;
uint8_t buttonMittel = 2;
uint8_t buttonKurz = 15;
uint8_t buttonUKW = 12;
uint8_t buttonSprMus = 13;

uint8_t potiPin = 25; // rechts -> 3,3v; links -> ground

uint8_t langKurzMittelEncoderA = 26; // grün
uint8_t langKurzMittelEncoderB = 27; // weiß

uint8_t ukwEncoderA = 32;
uint8_t ukwEncoderB = 33;

// ---------- do not edit -------------------
RotaryEncoder encoderLangKurzMittel(langKurzMittelEncoderA, langKurzMittelEncoderB, RotaryEncoder::LatchMode::FOUR3);
RotaryEncoder encoderUKW(ukwEncoderA, ukwEncoderB, RotaryEncoder::LatchMode::FOUR3);
static int posLangKurzMittel = 0;
static int posUKW = 0;

typedef struct { 
  uint8_t iterator;
  char* buttonName;
  uint8_t buttonPin;
} buttonStruct;
const buttonStruct myButtons[] {
    {0, "buttonOnOff", buttonOnOff},
    {1, "buttonLang", buttonLang},
    {2, "buttonMittel", buttonMittel},
    {3, "buttonKurz", buttonKurz},
    {4, "buttonUKW", buttonUKW},
    {5, "buttonSprMus", buttonSprMus}
};

unsigned char numberButtons = 5;
String output;
int a = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(500000);
}

void loop() {
  // read buttons
   unsigned long StartTime = micros();
  if ((a%1500) == 0)
  {
    output = "-";
    for(uint8_t i = 0; i < sizeof(myButtons)/sizeof(buttonStruct); ++i) {
      output += myButtons[i].buttonName;
      output += ":";
      output += readButton(myButtons[i].buttonPin);
      output += ",";
    }
    output += createPotiString(potiPin);
  }
  
  output += processEncoders();
  if ((a%1500) == 0)
  {
    Serial.println(output);
  }

  resetOutput();
  unsigned long CurrentTime = micros();
  unsigned long ElapsedTime = CurrentTime - StartTime;
  // Serial.println(ElapsedTime);
  a +=1;
}

String processEncoders()
{
  String returnString;

  encoderLangKurzMittel.tick();
  int newPosLangKurzMittel = encoderLangKurzMittel.getPosition();
  if (posLangKurzMittel != newPosLangKurzMittel) {
    posLangKurzMittel = newPosLangKurzMittel;
  }
  if (posLangKurzMittel < 0)
  {
    posLangKurzMittel = 0;
  }
  returnString = "posLangKurzMittel:";
  returnString += posLangKurzMittel;
  returnString += ",";

  encoderUKW.tick();
  int newPosUKW = encoderUKW.getPosition();
  if (posUKW != newPosUKW) {
    posUKW = newPosUKW;
  }
  if (posUKW < 0)
  {
    posUKW = 0;
  }
  returnString += "posUKW:";
  returnString += posUKW;
  returnString += ";";

  return returnString;
}

void resetOutput()
{
  output = "";
}

int readButton(uint8_t buttonPin )
{
  //touchAttachInterrupt(T2, gotTouch1, threshold);
  return touchRead(buttonPin);  
}

String createPotiString(int potiPin)
{
  int potiValue = analogRead(potiPin);
  String potiString = "potiValue:";
  potiString += potiValue;
  potiString += ","; 
  return potiString;
}
