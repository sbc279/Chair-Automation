# Chair Automation

# <div align="center">CONTRIBUTORS WELCOMED</div>

<b>I have no schematic or code reviewers, but I really could use another set of eyes on this. Also, although this device can successfully connect to a Wi-Fi access point, I could really use help accessing PICO's file system remotely (Telnet, SSH, etc.).<br /><div align="center"><i>I NEED SOMEONE'S EXPERTISE AND HELP!</i></div></b><br>
 
A powered chair is a must for a person with disabilities.

<b>The problem:</b><br>
Easily exiting the raised chair quickly diminishes because, after you are up, sadly the chair is also. It is difficult to sit back down in it when raised, and the only way to lower it is to reach down, press, and HOLD the “down” button until the chair is in the normal (home) position. Compounding to that, you must lean over even more as the chair lowers!

<b>The Solution:</b><br>
By placing this device "in line" with the chair's current buttons, it can lower it for you!

This device keeps your recliner's functionality and enhances it by using an optional added, generic button controller. The latch-like button abilities mean you no longer must press and hold a button! By incorporating a low-cost ($15) microprocessor, you can turn it into a 'smart' chair.

First off, to address the somewhat sloppy construction and/or appearance of the device: You see, I am disabled, battling MS for over 35 years (ahh, now it’s becoming clear why I even thought of building this thing, right?). I'm basically one-handed causing my fine motor skills, such as soldering or drilling holes in a straight line, well… to really suck. If you can manage to forgive that part, this device really can be beneficial and have influence. Who knows, maybe a couple of rainbow or unicorn stickers might make it pretty??

My background consists of being an FM radio broadcast engineer for nearly 15 years, eventually jumping ship and landing as a professional software (c#) engineer for the past 20+ years.

<b>The device:</b>

Just like I'm sure others with limited mobility already know, having a powered recliner is essential for getting up and out!

But after you're up, you must lean over and press and hold the "down" button to get the chair back to its normal position. Plus, as it gets further down you still must lean over that much more to hold the button.
This puts an end to that by introducing a level of automation to the chair, bed, or purposes yet to be realized. Allow me to explain:

This device draws its power from the chair's power supply, converting and conditioning it to 5vdc to power the microprocessor and relays. It has provisions for up to two controllers. The first, or "Main Controller", is the one that came with the chair and most likely built into it. Its function stays as it always has. Although now under this device's control, it is 100% operationally transparent. If the original controller/buttons have a light or USB charging port built-in to it, sadly neither will be operational. They will no longer have the 38-volt supplied to it/them.

The second controller is labeled "Logic Controller". This controller’s operation is where the magic happens, as detailed below.

It's important to realize that the two controllers are completely independent and interchangeable with each other, allowing you to use one or both as your situation warrants.

 Now, a couple of needed explanations before continuing:

<li>The term "Controller" is actually the up/down button array. This can be hand-held or built-in to the chair. Regardless, it will have a plug on the end of it's wire.</li>
<li>The “Home Position”: This is when the chair is in its “normal”, upright position; not reclined or lifted to exit.</li>
<li>The "Duration Time": This is how long the motor is engaged (in seconds). "Down" adds to the time, "Up" subtracts from it. When in the Home position, this value is always 0. As it reclines, the value gets higher. As the chair begins to lift, this value gets lower (and will be a negative value).</li>


<b>Pressing the Up button on the Logic Controller:</b>

If the chair is at its home position and/or the "Duration Time" is 0, the "up and out" process is activated, consisting of:
<li>The chair motor's "up" is engaged for an (adjustable) time (or optional mechanical limit switch, or both).</li>
<li>Pauses at the top for 10 seconds (adjustable) allowing time to exit.</li>
<li>Automatically activates motor "down" for an (adjustable) time (or optional mechanical home switch is activated*, or both).</li>

If the chair is at its home position and/or the "Duration Time" greater than 0, then it's assumed the chair is somewhere in a reclined position. Regardless, the motor "up" is engaged until the "home" switch is activated* (if used), or the "Duration Time" reaches 0.

 <b>Pressing the Down button on the Logic Controller:</b>

 If the chair is at its home position and/or the "Duration Time" greater than 0, it turns the motor "down" in 10 seconds (adjustable) increments.

If the chair is NOT in its home position and/or the "Duration Time" is less than 0, then it's assumed the chair is somewhere in the "lift" position.  Regardless, the motor "down" is engaged until the "home" switch is activated* (if used), or the "Duration Time" reaches 0.

This device always "knows" what position it’s at (assuming this device was started with the chair in its "normal" position) by counting how long the motor is engaged. "Down" adds to the time, "Up" subtracts from it.

Of course, that timing is not as important if you install the optional limit switches. Although there are optional Upper, Lower, and Occupancy switches, perhaps the most common (and most important) switch is the "Home" switch. This switch shows when the chair is in its "normal" position. From a programming perspective, once the "home" switch is activated*, the time is reset to zero.

If while any command is conducted, any button from either controller is pressed, the operation is halted and the chair waits for its next command.

This entire project is the combination of hardware and software. The microprocessor is controlled by the microPython programming language, the source code available on GitHub.

* The "Home" switch is activated any time there is a change in its state (open or closed)


