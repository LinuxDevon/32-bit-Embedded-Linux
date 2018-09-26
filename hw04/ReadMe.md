The overall goal of this project was to memory map with c and control a display.

# FILES
* Makefile - the make file to compile the two programs
* memoryMap.c - Uses to buttons to control the user LEDS
* toggleLED.c - Toggles the gpio pin to see how fast it can go using DMM
* beaglebone_gpio.h - the header to define GPIO ports and addresses
* homework4.docx - The pictures of the LCD working

# RUN
## memoryMap
To run the toogleLED you need to run `./config.sh` to configure the GPIO pins.

If you haven't compile the code with `make all`.

Next wire up the buttons to this pins and connect the other side to ground.
```
P9_42
P9_41
```

Run `sudo ./memoryMap` to start the program and push the buttons to see USR2 and USR3
leds toggle based on the buttons. Press ctrl-c to quit.

This part has been tested and verified by me.

## toggleLED
run `./config.sh` and `make all` if you haven't already done so.

connect a wire to `P9_15`. Attach a scope to that and GND then run `sudo ./toggleLED <us period>`
to see GPIO pin toggle.

I got mine to run around ~6kHz which is way faster than the other methods. There was a lot
of noise and misses though when viewed on the scope.

## LCD
I ran the video, picture, and text on the LCD and it was verified by Dr. Yoder.
You can see the homework4.docx file for pictures of it functioning.

========================
Professor Yoder's Comments

Looks very good.  Nice and complete.

Score:  10/10