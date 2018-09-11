#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

#include <libsoc_gpio.h>
#include <libsoc_debug.h>

// Blinks an LED attached to P9_12
#define GPIO_OUTPUT 60

// This program toggles an led on GPIO 60 1000000 times.
// You input the rate you want to blink at as an argument
// the rate is in microseconds

// this program doesn't check for valid time inputs

int main(int argc, char *argv[]) {
    
    // check input is valid 

    if(argc != 2 ) {
        printf("Invalid command. USAGE: ./blinkLED <delay(us)>\n");
        return -1;
    }
    
    int delay = atoi(argv[1]);
    
    gpio *gpio_output;      // Create gpio pointer
    libsoc_set_debug(1);    // Enable debug output
                           
    // Request gpio
    gpio_output = libsoc_gpio_request(GPIO_OUTPUT, LS_SHARED);
    
    // Set direction to OUTPUT
    libsoc_gpio_set_direction(gpio_output, OUTPUT);
    libsoc_set_debug(0);    // Turn off debug printing
                            // for fast toggle
                            
    int i;
    for (i=0; i<1000000; i++) { // Toggle GPIO X times
        libsoc_gpio_set_level(gpio_output, HIGH);
        usleep(delay/2);     
        libsoc_gpio_set_level(gpio_output, LOW);
        usleep(delay/2);
    }
    if (gpio_output) {
        // Free gpio request memory
        libsoc_gpio_free(gpio_output); 
        
    }
    
    return EXIT_SUCCESS;
}