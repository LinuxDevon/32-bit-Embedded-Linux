# Video Questions
1. Where does Julia Cartwright work?
	- National Instruments

2. What is PREEMT_RT? Hint: Google it.
	- It is a patch to the linux kernel that allows for premtion of processes during execution. It allows for real time applications to ensure your process is executed before a certain time.

3. What is mixed criticality?
	- There are different types of prioities when it comes to task on linux. Some are important and need to execute by a certain time (latency) while others are not as important and can wait a bit to execute.

4. How can drivers misbehave?
	- They can misbehave because of timing issues that arise with the realtime patch of being interrupted when they expect to execute without interruption. Having them in threads is one issue that use hard irqs in threads.

5. What is Δ in Figure 1?
	- It is the difference in the amount of time that the event happens till the time it executes. irq_dispatch + scheduling = delta

6. What is Cyclictest[2]?
	- It a way to measure the latency of task execution. It makes a sleep and takes a time stamp before the sleep and then measures the time right after the thread wakes up to see how long it has been.

7. What is plotted in Figure 2?
	- The cyclic test of the delta in figure one of the latency of the processes being executed. It compares the non prempt rt to the prempt rt process execution times.

8. What is dispatch latency? Scheduling latency?
	- Dispatch latency is the amount time from the hardware irq firing till the time the thread scheduler gets told that the thread needs to run.
	- Scheduling latency is the time it takes from being told the thread with the irq needs to be run till the actual execution of the thread on the cpu.

9. What is mainline?
	- Mainline is the most up to date Linux Kernel that has the newest features.

10. What is keeping the External event in Figure 3 from starting?
	- It has to wait for the other lower prioity process to to finish before it can execute.

11. Why can the External event in Figure 4 start sooner?
	- They force irq threads to execute. They have small chunks of code wake up the higher prioity threads to make them execute over lower prioity threads.
