// Pi power button

// A single Pi PI_COM pin is used, plus connections to the Pi's TxD and SCL, which don't affect their
// normal use. TxD is the only pin which will reliably indicate that the Pi is shutdown.
//
// The Pi sets its PI_COM pin as Input Pullup and watches for a Low to signal a shutdown request.
// On seeing this it sets the PI_COM as Output, Low to acknowledge the request.
// When shutdown completes, TxD goes low. If the Pi is rebooted, it goes high again.
//
// The ATTiny has a pin configured as Output, set High, and connected to the Pi through 330 Ohms.
// On pressing the button, this pin is pulled Low for 500mS, then set as Input Pullup.
//
// If it sees the PI_COM pin now Low it starts flashing the LED and awaits TxD to go low.
//

#define LED PB4  //25             // Pin 6            // POWER LED
#define RELAY PB1     //33        // Pin 2            // TURNS ON POWER TO RASPI
#define PI_ACTIVE PB3 //4         // Pin 3 -> RPI 5   // PI_ACTIVE should get ON at boot and off right after shutdown
#define PI_COM PB0 //19           // PB0 -> RPi 5/14    // Used to communicate with raspberry
#define BUTTON PB2 //32           //         // DETECTS ON/OFF REQUEST
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

bool relayState = false;

void setup() {     
  //Serialbegin(115200);           
  //delay(1000);
  //Serialprintln("STARTING 222");
  pinMode(LED, OUTPUT);
  pinMode(BUTTON, INPUT_PULLUP);
  pinMode(PI_COM, OUTPUT); // Pi PI_COM pin
  pinMode(PI_ACTIVE, INPUT); // Pi PI_ACTIVE pin
  //pinMode(SCL, INPUT);
  digitalWrite(LED, LOW);
  digitalWrite(PI_COM, HIGH);
  
  pinMode(RELAY, OUTPUT);
  //Serialprintln ("RELAY HIGH");
  delay(10);
  digitalWrite(RELAY, LOW);
  relayState = false;

  prevstate = NOT_INIT; 
  state = OFF_STATE;
  timeout = txdtimer = buttontimer = timer = 0;
  //Serialprintln("STARTING");
}

// loop runs forever and ever:
void loop() {
  //delay(100);
  int val;
  long count, t;
  switch (state) {
    case OFF_STATE: // OFF
    default:
      processOffState();
      break;

    // TODO: instead of pull SCL high just give power to the raspberry
    case START_BOOT_STATE: // BOOT START
      processStartBootState();
      break;

    case BOOTING_STATE: // BOOTING
      processBootingState();
      break;

    case ON_STATE: // ON
      processOnState();
      break;

    case START_SHUTDOWN_STATE: 
      processStartShutdownState();
      break;

    case SHUTTING_DOWN_STATE: 
      processShuttingDown();
      break;
  }
  delay(50);
}

void processOffState() {
  // ---- OFF STATE DEFINITION ----
  // LED: OFF
  // If Button press -> START_BOOT
  // If TXD high -> BOOTING

  if (state != prevstate) {
    //Serialprint("Off\n");
    prevstate = state;
  }
  pinMode(PI_COM, INPUT_PULLUP);
  digitalWrite(LED, LOW);
  // digitalWrite(LED, ((millis() - timer) / 5000) % 2 == 0);

  // check button press
  if (digitalRead(BUTTON) == HIGH) {
    buttontimer = millis();
  } else {
    if (millis() - buttontimer > 50) {
      //Serialprintln("BUTTON CLICKED START BOOT");
      if (!relayState) {
       // digitalWrite(RELAY, HIGH);
        //relayState = true;
        delay(100);
      } 
      state = START_BOOT_STATE; // BOOT REQ
      return;
    }
  }

  // TXD HIGH means raspi is already on
  if (digitalRead(PI_ACTIVE) == HIGH) {
    //Serialprintln("TXD HIGH. IN BOOT");
    state = BOOTING_STATE; // BOOTING
    return;
  }
  return;
}

void processStartBootState() {
  // ---- START BOOT DEFINITION ----
  // LED: OFF
  // RELAY: ON
  // If TXD high then State = 2 (BOOTING)
  // If timeout 50mS then State = 0 (OFF)
  if (state != prevstate) 
  {
    //Serialprint("Boot Req\n");
    // TURN ON RASPI
    pinMode(RELAY, OUTPUT);
    digitalWrite(RELAY, LOW);
    relayState = false;
    delay(50);
    txdtimer = millis();
    prevstate = state;
  }

   digitalWrite(LED, ((millis() - timer) / 1000) % 2 == 0);
  if (digitalRead(PI_ACTIVE) == HIGH) {
    //Serialprintln("PI_ACTIVE HIGH. IN BOOT");
    state = BOOTING_STATE; // BOOTING
    return;
  }
  if (millis() - txdtimer > 50) {
    // GO TO OFF AND WAIT TILL TXD is HIGH
    state = OFF_STATE; // OFF
  }
  return;
}

void processBootingState() {
  // ---- START BOOT DEFINITION ----
  // LED: FON
  // Wait for Pi to set PI_COM input pullup
  // Poll Pi by pulsing PI_COM low for 5mS
  // If PI_COM low pulse acknowledged then State = 3 (RUNNING)
  // If TXD low then State = 0 (OFF)
  // If timeout 50 secs then State = 3 (RUNNING)
  if (state != prevstate) {
    //Serialprint("Booting\n");
    timer = millis();
    prevstate = state;
  }

  // digitalWrite(LED, HIGH);
  digitalWrite(LED, ((millis() - timer) / 1000) % 4 == 0);

  if (digitalRead(PI_COM) == LOW) {
    //Serialprintln("LOW");
    return;
  }

  if ((millis() - timer) % 100 == 50) {
    pinMode(PI_COM, OUTPUT);
    digitalWrite(PI_COM, LOW);
    delay(5);
    digitalWrite(PI_COM, HIGH);
    pinMode(PI_COM, INPUT_PULLUP);
    timeout = millis();
    while (millis() - timeout < 100) {
      //Serialprintln("HELLO");
      delay(1);
      if (digitalRead(PI_COM) == HIGH) {
        //Serialprintln("WAIT FOR LOW");
        continue;
      }
      //Serialprintln("RasPi PI_COM LOW. Must be on");
      state = ON_STATE; // RUNNING
      return;
    }
    while (digitalRead(PI_COM) == LOW) continue;
    pinMode(PI_COM, OUTPUT);
    digitalWrite(PI_COM, HIGH);
    if (state != prevstate) return;
  }
  if (digitalRead(PI_ACTIVE) == LOW) {
    //Serialprintln("TXD LOW. Raspberry must be off");
    state = OFF_STATE; // OFF
    return;
  }
  if ((millis() - timer) > 50000) {
    //Serialprintln("TIMER HIT END. BOOTING FINISHED");
    state = ON_STATE; // ON
  }
}

void processBootingState2() {
      if (state != prevstate) {
      //Serialprint("Booting\n");
      timer = millis();
      prevstate = state;
    }
    digitalWrite(LED, HIGH);
    if (digitalRead(PI_COM) == LOW) return;
    if ((millis() - timer) % 100 == 50) {
      //Serialprint("Poll\n");
      pinMode(PI_COM, OUTPUT);
      digitalWrite(PI_COM, LOW);
      delay(5);
      digitalWrite(PI_COM, HIGH);
      pinMode(PI_COM, INPUT_PULLUP);
      timeout = millis();
      while (millis() - timeout < 100) {
        delay(1);
        if (digitalRead(PI_COM) == HIGH) continue;
        state = ON_STATE; // RUNNING
        return;
      }
      while (digitalRead(PI_COM) == LOW) continue;
      pinMode(PI_COM, OUTPUT);
      digitalWrite(PI_COM, HIGH);
      if (state != prevstate) return;
    }
    if (digitalRead(PI_ACTIVE) == LOW) {
      state = OFF_STATE; // OFF
      return;
    }
    if ((millis() - timer) > 20000) {
      state = ON_STATE; // RUNNING
      //Serialprintln("TIMER HIT END. BOOTING FINISHED");
    } 
    return;
}
void processOnState() {
  // LED on
  // PI_COM high
  // If TXD low then State = 0 (OFF)
  // If button push then State = 4 (SHDN REQ)
  if (state != prevstate) {
    //Serialprint("Running\n");
    pinMode(PI_COM, OUTPUT);
    digitalWrite(PI_COM, HIGH);
    prevstate = state;
  }
  // digitalWrite(LED, ((millis() - timer) / 20) % 8 != 0);
  digitalWrite(LED, HIGH);
  if (digitalRead(PI_ACTIVE) == HIGH) txdtimer = millis();
  else {
    if ((millis() - txdtimer) > 50) {
      //Serialprintln("TXD LOW. Raspberry must be off");
      state = OFF_STATE; // OFF
      return;
    }
  }
  if (digitalRead(BUTTON) == HIGH) {
    buttontimer = millis();
  } else if (millis() - buttontimer > 1000) {
    //Serialprintln("Button HIGH. Wants shutdown");
    state = START_SHUTDOWN_STATE; // SHDN REQ
    return;
  }
  return;
}
      
void processStartShutdownState() {
  // SHDN REQ
  // Pulse PI_COM low
  // LED off
  // If PI_COM low then State = 5 (SHUTTING DOWN)
  // If TxD low then State = 0 (OFF)
  // Timeout 100mS then 3 (RUNNING)
  if (state != prevstate) {
    //Serialprint("Shutdown Req\n");
    digitalWrite(LED, ((millis() - timer) / 20) % 8 == 0);
    pinMode(PI_COM, OUTPUT);
    digitalWrite(PI_COM, LOW);
    //Serialprintln("TO LOW");
    delay(500);
    pinMode(PI_COM, INPUT_PULLUP);
    timer = millis();
    prevstate = state;
  }
  if (digitalRead(PI_COM) == LOW) {
    state = SHUTTING_DOWN_STATE; // SHUTTING DOWN
    return;
  }
  if (digitalRead(PI_ACTIVE) == HIGH) txdtimer = millis();
  else {
    if (millis() - txdtimer > 200) {
      state = SHUTTING_DOWN_STATE; // OFF
      return;
    }
  }
  if ((millis() - timer) > 400) {
    state = ON_STATE; // RUNNING
    return;
  }
  return;
}

void processShuttingDown() {
  // SHUTTING DOWN
  // Flash LED 75% duty cycle
  // If TXD low then State = 0 (OFF)
  // If timeout 20 secs then State = 3 (RUNNING)
  if (state != prevstate) {
    //Serialprint("Shutting down\n");
    timer = millis();
    prevstate = state;
  }
  
  digitalWrite(LED, ((millis() - timer) / 20) % 4 != 0);
  if (digitalRead(PI_ACTIVE) == HIGH) txdtimer = millis();
  else {
    //for safety reason wait 7s and then cut power
    if (millis() - txdtimer > 10000) {
      // Cutting power
      //Serialprintln("CUTTING POWER");
      digitalWrite(RELAY, HIGH);
      relayState = true;
      state = OFF_STATE; // OFF
      return;
    }
  }
  if ((millis() - timer) > 15000) {
      digitalWrite(RELAY, HIGH);
      relayState = true;
      state = OFF_STATE; // OFF
    return;
  }
  return;
}

