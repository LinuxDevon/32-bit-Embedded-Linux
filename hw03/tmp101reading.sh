#!/bin/sh
echo "reading temp sensor on i2c..."

# -- TEMP 1 -- #
temp1Raw=`i2cget -y 2 0x48`
temp1F=$(($temp1Raw*9/5+32))
echo "temp1 =" $temp1F "degF"

# -- TEMP 2 -- #
temp2Raw=`i2cget -y 2 0x49`
temp2F=$(($temp2Raw*9/5+32))
echo "temp2 =" $temp2F "degF"