
// msoe supermileage

void setup() {
    Serial.begin(9600);
}

void loop() {
    // speeds between 0 and 45 mph
    long rand = random(45);
    double speed = 1.0 * rand;

    // wait inversely proportional to speed
    double wait_time_ms = 1.0/speed;

    // don't wait longer than half a second if we slow down significantly
    if (wait_time_ms > 500.0) {
	wait_time_ms = 500.0;
    }

    // don't send too fast either (?)
    if (wait_time_ms < 10.0) {
	wait_time_ms = 10.0;
    }
    
    delay((long) wait_time_ms);
    Serial.println(speed);
}

