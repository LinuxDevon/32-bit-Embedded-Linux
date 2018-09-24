// From : http://stackoverflow.com/questions/13124271/driving-beaglebone-gpio-through-dev-mem
//
// Be sure to set -O3 when compiling.
// Modified by Mark A. Yoder  26-Sept-2013
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h> 
#include <time.h>
#include <signal.h>    // Defines signal-handling functions (i.e. trap Ctrl-C)
#include "beaglebone_gpio.h"

/****************************************************************
 * Global variables
 ****************************************************************/
int keepgoing = 1;    // Set to 0 when ctrl-c is pressed

/****************************************************************
 * signal_handler
 ****************************************************************/
void signal_handler(int sig);
// Callback called when SIGINT is sent to the process (Ctrl-C)
void signal_handler(int sig)
{
	printf( "\nCtrl-C pressed, cleaning up and exiting...\n" );
	keepgoing = 0;

}

int main(int argc, char *argv[]) {
    volatile void *gpio_addr0, *gpio_addr1;
    volatile unsigned int *gpio_oe_addr1;
    volatile unsigned int *gpio_datain_addr0;
    volatile unsigned int *gpio_setdataout_addr1;
    volatile unsigned int *gpio_cleardataout_addr1;
    unsigned int reg;
    
    // Set the signal callback for Ctrl-C
	signal(SIGINT, signal_handler);

    int fd = open("/dev/mem", O_RDWR);

    // The Buttons on "P9_41/42"
    printf("Mapping %X - %X (size: %X)\n", GPIO0_START_ADDR, GPIO0_END_ADDR, GPIO0_SIZE);

    gpio_addr0 = mmap(0, GPIO0_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, GPIO0_START_ADDR);

    gpio_datain_addr0 = gpio_addr0 + GPIO_DATAIN;

    if(gpio_addr0 == MAP_FAILED) {
        printf("Unable to map GPIO\n");
        exit(1);
    }
    
    // Map the user LEDs 3 and 2
    printf("Mapping %X - %X (size: %X)\n", GPIO1_START_ADDR, GPIO1_END_ADDR, GPIO1_SIZE);

    gpio_addr1 = mmap(0, GPIO1_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, GPIO1_START_ADDR);

    gpio_oe_addr1           = gpio_addr1 + GPIO_OE;
    gpio_setdataout_addr1   = gpio_addr1 + GPIO_SETDATAOUT;
    gpio_cleardataout_addr1 = gpio_addr1 + GPIO_CLEARDATAOUT;

    if(gpio_addr1 == MAP_FAILED) {
        printf("Unable to map GPIO\n");
        exit(1);
    }

    // Set USR3 to be an output pin
    reg = *gpio_oe_addr1;
    reg &= ~USR3;       // Set USR3 bit to 0
    *gpio_oe_addr1 = reg;
    
    // Set USR2 to be an output pin
    reg = *gpio_oe_addr1;
    reg &= ~USR2;       // Set USR2 bit to 0
    *gpio_oe_addr1 = reg;

    printf("Running and waiting for button presses...\n");
    while(keepgoing) {
        // wait for button one to be pressed. 
        if((*gpio_datain_addr0 & GPIO_20) == 0) {
            *gpio_setdataout_addr1 = USR3;
        } else {
            *gpio_cleardataout_addr1  = USR3;
        }
        
        // wait for button one to be pressed. 
        if((*gpio_datain_addr0 & GPIO_07) == 0) {
            *gpio_setdataout_addr1 = USR2;
        } else {
            *gpio_cleardataout_addr1 = USR2;
        }
        usleep(1); // timing for global variable

    }

    munmap((void *)gpio_addr0, GPIO0_SIZE);
    munmap((void *)gpio_addr1, GPIO1_SIZE);
    close(fd);
    return 0;
}
