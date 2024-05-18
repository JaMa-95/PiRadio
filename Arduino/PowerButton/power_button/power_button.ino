// Pi power button

// A single Pi GPIO_PI pin is used, plus connections to the Pi's TxD and SCL, which don't affect their
// normal use. TxD is the only pin which will reliably indicate that the Pi is shutdown.
//
// The Pi sets its GPIO_PI pin as Input Pullup and watches for a Low to signal a shutdown request.
// On seeing this it sets the GPIO_PI as Output, Low to acknowledge the request.
// When shutdown completes, TxD goes low. If the Pi is rebooted, it goes high again.
//
// The ATTiny has a pin configured as Output, set High, and connected to the Pi through 330 Ohms.
// On pressing the button, this pin is pulled Low for 500mS, then set as Input Pullup.
//
// If it sees the GPIO_PI pin now Low it starts flashing the LED and awaits TxD to go low.
//

#define LED 4 // Pin 6
#define RELAY 1 // Pin 2
#define TXD 3 // Pin 3
#define GPIO_PI 0     // PB0
#define BUTTON 2 // ????????
// Gnd 4
// Vcc 8


#define OFF_STATE 0
#define START_BOOT_STATE 1
#define BOOTING_STATE 2
#define ON_STATE 3
#define START_SHUTDOWN_STATE 4
#define SHUTTING_DOWN_STATE 5
#define NOT_INIT 99

int state, prevstate;
long int timeout, txdtimer, buttontimer, timer;

void setup() {                
  pinMode(LED, OUTPUT);
  pinMode(BUTTON, INPUT_PULLUP);
  pinMode(GPIO_PI, OUTPUT); // Pi GPIO_PI pin
  pinMode(TXD, INPUT); // Pi TxD pin
  //pinMode(SCL, INPUT);
  digitalWrite(LED, LOW);
  digitalWrite(GPIO_PI, HIGH);
 // //Serial.begin(9600);
  pinMode(RELAY, OUTPUT);
  // //Serial.println ("RELAY HIGH");
  digitalWrite(RELAY, HIGH);

  prevstate = NOT_INIT; 
  state = timeout = txdtimer = buttontimer = timer = 0;
}

// loop runs forever and ever:
void loop() {
  //delay(100);
  int val;
  long count, t;
  switch (state) {
    case OFF_STATE: // OFF
    default:
    // ---- OFF STATE DEFINITION ----
    // LED: OFF
    // If Button press -> START_BOOT
    // If TXD high -> BOOTING

    if (state != prevstate) {
      ////Serial.print("Off\n");
      prevstate = state;
    }
    pinMode(GPIO_PI, INPUT_PULLUP);
    //digitalWrite(LED, LOW);
    digitalWrite(LED, ((millis() - timer) / 250) % 4 == 0);
    if (digitalRead(BUTTON) == HIGH) {
      buttontimer = millis();
    } else {
      if (millis() - buttontimer > 50) {
        //Serial.println("BUTTON CLICKED START BOOT");
        state = START_BOOT_STATE; // BOOT REQ
        break;
      }
    }
    if (digitalRead(TXD) == HIGH) {
      //Serial.println("TXD HIGH. IN BOOT");
      state = BOOTING_STATE; // BOOTING
      break; 
    }
    break;

    // TODO: instead of pull SCL high just give power to the raspberry
    case START_BOOT_STATE: // BOOT START
    // ---- START BOOT DEFINITION ----
    // LED: OFF
    // RELAY: ON
    // If TXD high then State = 2 (BOOTING)
    // If timeout 50mS then State = 0 (OFF)
    if (state != prevstate) 
    {
      //Serial.print("Boot Req\n");
      pinMode(RELAY, OUTPUT);
      digitalWrite(RELAY, LOW);
      delay(50);
      txdtimer = millis();
      prevstate = state;
    }

    digitalWrite(LED, LOW);
    if (digitalRead(TXD) == HIGH) {
      //Serial.println("TXD HIGH. IN BOOT");
      state = BOOTING_STATE; // BOOTING
      break;
    }
    if (millis() - txdtimer > 50) {
      // GO TO OFF AND WAIT TILL TXD is HIGH
      state = OFF_STATE; // OFF
    }
    break;

    case BOOTING_STATE: // BOOTING
    // ---- START BOOT DEFINITION ----
    // GPIO_PI: HIGH
    // LED: Flash 25% duty cycle
    // Wait for Pi to set GPIO_PI input pullup
    // Poll Pi by pulsing GPIO_PI low for 5mS
    // If GPIO_PI low pulse acknowledged then State = 3 (RUNNING)
    // If TXD low then State = 0 (OFF)
    // If timeout 50 secs then State = 3 (RUNNING)
    if (state != prevstate) {
      //Serial.print("Booting\n");
      timer = millis();
      prevstate = state;
    }

    digitalWrite(LED, ((millis() - timer) / 250) % 4 == 0);

    if (digitalRead(GPIO_PI) == LOW) break;

    if ((millis() - timer) % 100 == 50) {
      pinMode(GPIO_PI, OUTPUT);
      digitalWrite(GPIO_PI, LOW);
      delay(5);
      digitalWrite(GPIO_PI, HIGH);
      pinMode(GPIO_PI, INPUT_PULLUP);
      timeout = millis();
      while (millis() - timeout < 100) {
        delay(1);
        if (digitalRead(GPIO_PI) == HIGH) {
          continue;
        }
        //Serial.println("RasPi GPIO_PI LOW. Must be on");
        state = ON_STATE; // RUNNING
        break;
      }
      while (digitalRead(GPIO_PI) == LOW) continue;
      pinMode(GPIO_PI, OUTPUT);
      digitalWrite(GPIO_PI, HIGH);
      if (state != prevstate) break;
    }
    if (digitalRead(TXD) == LOW) {
      //Serial.println("TXD LOW. Raspberry must be off");
      state = OFF_STATE; // OFF
      break;
    }
    if ((millis() - timer) > 50000) {
      //Serial.println("TIMER HIT END. BOOTING FINISHED");
      state = ON_STATE; // ON
    }
    break;

    case ON_STATE: // ON
    // LED on
    // GPIO_PI high
    // If TXD low then State = 0 (OFF)
    // If button push then State = 4 (SHDN REQ)
    if (state != prevstate) {
      //Serial.print("Running\n");
      pinMode(GPIO_PI, OUTPUT);
      digitalWrite(GPIO_PI, HIGH);
      prevstate = state;
    }
    digitalWrite(LED, ((millis() - timer) / 20) % 8 != 0);
    if (digitalRead(TXD) == HIGH) txdtimer = millis();
    else {
      if ((millis() - txdtimer) > 50) {
        //Serial.println("TXD LOW. Raspberry must be off");
        state = OFF_STATE; // OFF
        break;
      }
    }
    if (digitalRead(BUTTON) == HIGH) {
      buttontimer = millis();
    } else if (millis() - buttontimer > 1000) {
      //Serial.println("RasPi GPIO_PI HIGH. Wants shutdown");
      state = START_SHUTDOWN_STATE; // SHDN REQ
      break;
    }
    break;

      case START_SHUTDOWN_STATE: // SHDN REQ
      // Pulse GPIO_PI low
      // LED off
      // If GPIO_PI low then State = 5 (SHUTTING DOWN)
      // If TxD low then State = 0 (OFF)
      // Timeout 100mS then 3 (RUNNING)
      if (state != prevstate) {
        //Serial.print("Shutdown Req\n");
        digitalWrite(LED, LOW);
        pinMode(GPIO_PI, OUTPUT);
        digitalWrite(GPIO_PI, LOW);
        delay(500);
        pinMode(GPIO_PI, INPUT_PULLUP);
        timer = millis();
        prevstate = state;
      }
      if (digitalRead(GPIO_PI) == LOW) {
        state = SHUTTING_DOWN_STATE; // SHUTTING DOWN
        break;
      }
      if (digitalRead(TXD) == HIGH) txdtimer = millis();
      else {
        if (millis() - txdtimer > 50) {
          state = OFF_STATE; // OFF
          break;
        }
      }
      if ((millis() - timer) > 100) {
        state = ON_STATE; // RUNNING
        break;
      }
      break;

    case SHUTTING_DOWN_STATE: // SHUTTING DOWN
    // Flash LED 75% duty cycle
    // If TXD low then State = 0 (OFF)
    // If timeout 20 secs then State = 3 (RUNNING)
    if (state != prevstate) {
      //Serial.print("Shutting down\n");
      timer = millis();
      prevstate = state;
    }
    digitalWrite(LED, ((millis() - timer) / 20) % 4 != 0);
    if (digitalRead(TXD) == HIGH) txdtimer = millis();
    else {
      if (millis() - txdtimer > 50) {
        // Cutting power
        pinMode(RELAY, OUTPUT);
        digitalWrite(RELAY, HIGH);
        state = OFF_STATE; // OFF
        break;
      }
    }
    if ((millis() - timer) > 20000) {
      state = ON_STATE; // RUNNING
      break;
    }
    break;
  }
}

