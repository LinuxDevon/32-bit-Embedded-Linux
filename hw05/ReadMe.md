The overall objective was to understand the kernel more. 

# FILES
* make
  * Makefile - The make file that i created to learn make and compile the helloworld program.
  * app.c - This is the test helloworld program.
  * path.mak - This is the include that has compiler information and to demo include in make.
* Beagle_Execution.png - Output from compiling on host and running on host.
* compile_native.png - Output from compiling on host and running on bone.
* part1_kernel_modules.png - Part one of kernel module example output.
* Part2_kernel_modules.png - Part two of kernel module example output.
* part3_kernel_module.png  Part three of kernel module example output.

# PROJECT
I have added some ideas to the page and added my name on ones I found interesting.

# MAKE
The files for this part are in the make folder.

To run you need to do `make` or `make all` then do `./app.arm` to execute the program.

You can remove the old files by typing `make clean`. `app.o` and `app.arm` will be deleted.

To see the variables of the make file type `make test`.

# KERNEL SOURCE
I have successfully compiled and installed the kernel and I am now on 4.19.

# CROSS-COMPILING
I have completed this and successfully ran on the program on the host and the bone. See the pictures below:
```
Beagle_Execution.png
compile_native.png
```

# KERNEL MODULES
I have successfully completed parts 1,2,3(example1). example 1 has been verified and the pictures show
the output of all the parts.
```
part1_kernel_modules.png
Part2_kernel_modules.png
part3_kernel_module.png 
```
