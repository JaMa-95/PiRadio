#include <RotaryEncoder.h>
#include <Arduino.h>

// 2. Rotary Encoder
// 1. absolut encoder -> Lautstärke

uint8_t potiPin = 25; // rechts -> 3,3v; links -> ground

uint8_t langKurzMittelEncoderA = 32; // grün
uint8_t langKurzMittelEncoderB = 33; // weiß

uint8_t ukwEncoderA = 27;
uint8_t ukwEncoderB = 26;

// ---------- do not edit -------------------
RotaryEncoder encoderLangKurzMittel(langKurzMittelEncoderA, langKurzMittelEncoderB, RotaryEncoder::LatchMode::FOUR3);
RotaryEncoder encoderUKW(ukwEncoderA, ukwEncoderB, RotaryEncoder::LatchMode::FOUR3);
static int posLangKurzMittel = 0;
static int posUKW = 0;


String output;
int a = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(500000);
}

void loop() {
  // read buttons
  output = "-";
  output += createPotiString(potiPin);
  output += processEncoders();
  if ((a%1000) == 0)
  {
    Serial.println(output);
  }

  resetOutput();
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
