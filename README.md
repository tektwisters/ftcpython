# ftcpython

How to build:

1. Open apk_python32 as an exsisting Android Studio project

2. Build with Android Studio

3. Put the ftc folder in the root of the internal sdcard of the Android device

4. Build the FTC SDK with the PythonOp opmode in it

How to use:

1. Open the PythonAPK app and it should create a notification that states that it is running. And it should also give two toasts that state "Starting server..." and "Listening for clients...".

2. Then open the FTC Robot Controller app

3. On the driver station open the FTC Driver Station app and select the PythonOp opmode and press start

4. If everything worked correctly then in the telemetry area it should say "Looped X times" with X being some number.

How to customize:

Simply edit the main.py script that is in the ftc folder on the Android device. By making classes that contain a "start" and a "loop" function you can make your own scripts.
