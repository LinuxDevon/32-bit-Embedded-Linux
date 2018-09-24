CFLAGS  := -O3 -g

#
# Programs
#
all:	memoryMap toggleLED

memoryMap: memoryMap.c beaglebone_gpio.h
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $<
	
toggleLED: toggleLED.c beaglebone_gpio.h
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $<

#
# Objects
#

%.o: %.c
	$(CC) $(CFLAGS) $(TOOLS_CFLAGS) -c $< -o $@

clean:
	rm memoryMap
