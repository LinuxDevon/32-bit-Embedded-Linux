#!/bin/sh
# -- TEMP 1 -- #
temp1Raw=`i2cget -y 2 0x48`
temp1F=$(($temp1Raw*9/5+32))
echo "temp1 =" $temp1F "degF"

# -- TEMP 2 -- #
temp1Raw=`i2cget -y 2 0x49`
temp1F=$(($temp1Raw*9/5+32))
echo "temp2 =" $temp1F "degF"