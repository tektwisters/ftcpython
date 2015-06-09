package com.qualcomm.ftcrobotcontroller.opmodes;

import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.app.Activity;
import android.widget.Toast;

import com.qualcomm.ftcrobotcontroller.FtcRobotControllerActivity;
import com.qualcomm.robotcore.eventloop.opmode.OpMode;
import com.qualcomm.robotcore.hardware.DcMotor;
import com.qualcomm.robotcore.hardware.Gamepad;
import com.qualcomm.robotcore.hardware.IrSeekerSensor;
import com.qualcomm.robotcore.hardware.Servo;
import com.qualcomm.robotcore.robocol.Telemetry;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.HashMap;
import java.util.Map;
import java.util.Objects;

/**
 * An empty op mode serving as a template for custom OpModes
 */
public class PythonOp extends OpMode {

    public  void startPythonActivity() {
        Context context = hardwareMap.appContext;
        Intent intent = context.getPackageManager().getLaunchIntentForPackage("com.android.python27");
        if (intent != null) {
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            context.startActivity(intent);
        }
    }

    boolean running;

    class MyClientTask extends Thread {
        String ipaddress;
        int portnumber;
        Map<String,DcMotor> motors = new HashMap<String,DcMotor>();
        Map<String,Servo> servos = new HashMap<String,Servo>();
        Map<String,IrSeekerSensor> irSensors = new HashMap<String,IrSeekerSensor>();

        MyClientTask(String ip, int port) {
            ipaddress = ip;
            portnumber = port;
        }

        @Override
        public void run() {
            boolean worked = false;
            while (!worked) {
                try {
                    Socket sock = new Socket(ipaddress, portnumber);

                    worked = true;

                    OutputStream ostream = sock.getOutputStream();
                    PrintWriter pwrite = new PrintWriter(ostream, true);

                    InputStream istream = sock.getInputStream();
                    BufferedReader receiveRead = new BufferedReader(new InputStreamReader(istream));

                    boolean keep = true;

                    String receiveMessage;
                    //                    sendMessage = "test";
//                    pwrite.println(sendMessage);
//                    pwrite.flush();
                    while (keep) {
                        if ((receiveMessage = receiveRead.readLine()) != null) {
                            char[] charArray = receiveMessage.toCharArray();
                            String[] args = receiveMessage.split(",");
                            switch (charArray[0]) {
                                case 'A':
                                    //Set motor
                                    double power = Double.valueOf(args[2]);
                                    motors.get(args[1]).setPower(power);
                                    break;
                                case 'B':
                                    //telemetry
                                    String key = args[1];
                                    String data = args[2];
                                    telemetry.addData(key, data);
                                    break;
                                case 'C':
                                    //running
                                    String result;
                                    if (running) {
                                        result = "1";
                                    } else {
                                        result = "0";
                                    }
                                    pwrite.println(result);
                                    pwrite.flush();
                                    if (!running) {
                                        keep = false;
                                    }
                                    break;
                                case 'D':
                                    //initMotor
                                    motors.put(args[1], hardwareMap.dcMotor.get(args[1]));
                                    if (args[2].equals("1")) {
                                        motors.get(args[1]).setDirection(DcMotor.Direction.REVERSE);
                                    }
                                    break;
                                case 'E':
                                    //initServo
                                    servos.put(args[1], hardwareMap.servo.get(args[1]));
                                    break;
                                case 'F':
                                    //setServo
                                    float value = Float.parseFloat(args[2]);
                                    servos.get(args[1]).setPosition(value);
                                    pwrite.println(args[2]);
                                    pwrite.flush();
                                    break;
                                case 'G':
                                    //initIrSensor
                                    irSensors.put(args[1], hardwareMap.irSeekerSensor.get(args[1]));
                                    break;
                                case 'H':
                                    //signalDetected
                                    String _result;
                                    boolean signal = irSensors.get(args[1]).signalDetected();
                                    if (signal) {
                                        _result = "1";
                                    } else {
                                        _result = "0";
                                    }
                                    pwrite.println(_result);
                                    pwrite.flush();
                                    break;
                                case 'I':
                                    //getAngle
                                    double angle = irSensors.get(args[1]).getAngle();
                                    pwrite.println(Double.valueOf(angle).toString());
                                    pwrite.flush();
                                    break;
                                case 'J':
                                    //getStrength
                                    double strength = irSensors.get(args[1]).getStrength();
                                    pwrite.println(Double.valueOf(strength).toString());
                                    pwrite.flush();
                                    break;
                                case 'K':
                                    //getControllerValue
                                    boolean pressed;
                                    double joyval;
                                    Gamepad gamepad;
                                    if (args[1].equals("1")) {
                                        gamepad = gamepad1;
                                    } else {
                                        gamepad = gamepad2;
                                    }
                                    switch (args[2]) {
                                        case "a":
                                            pressed = gamepad.a;
                                            if (pressed) {
                                                pwrite.println("1");
                                            } else {
                                                pwrite.println("0");
                                            }
                                            pwrite.flush();
                                            break;
                                        case "b":
                                            pressed = gamepad.b;
                                            if (pressed) {
                                                pwrite.println("1");
                                            } else {
                                                pwrite.println("0");
                                            }
                                            pwrite.flush();
                                            break;
                                        case "x":
                                            pressed = gamepad.x;
                                            if (pressed) {
                                                pwrite.println("1");
                                            } else {
                                                pwrite.println("0");
                                            }
                                            pwrite.flush();
                                            break;
                                        case "y":
                                            pressed = gamepad.y;
                                            if (pressed) {
                                                pwrite.println("1");
                                            } else {
                                                pwrite.println("0");
                                            }
                                            pwrite.flush();
                                            break;
                                        case "rsx":
                                            joyval = gamepad.right_stick_x;
                                            pwrite.println(Double.valueOf(joyval).toString());
                                            pwrite.flush();
                                            break;
                                        case "rsy":
                                            joyval = gamepad.right_stick_y;
                                            pwrite.println(Double.valueOf(joyval).toString());
                                            pwrite.flush();
                                            break;
                                        case "lsx":
                                            joyval = gamepad.left_stick_x;
                                            pwrite.println(Double.valueOf(joyval).toString());
                                            pwrite.flush();
                                            break;
                                        case "lsy":
                                            joyval = gamepad.left_stick_y;
                                            pwrite.println(Double.valueOf(joyval).toString());
                                            pwrite.flush();
                                            break;
                                        case "du":
                                            pressed = gamepad.dpad_up;
                                            if (pressed) {
                                                pwrite.println("1");
                                            } else {
                                                pwrite.println("0");
                                            }
                                            pwrite.flush();
                                            break;
                                        case "dd":
                                            pressed = gamepad.dpad_down;
                                            if (pressed) {
                                                pwrite.println("1");
                                            } else {
                                                pwrite.println("0");
                                            }
                                            pwrite.flush();
                                            break;
                                        case "dl":
                                            pressed = gamepad.dpad_left;
                                            if (pressed) {
                                                pwrite.println("1");
                                            } else {
                                                pwrite.println("0");
                                            }
                                            pwrite.flush();
                                            break;
                                        case "dr":
                                            pressed = gamepad.dpad_right;
                                            if (pressed) {
                                                pwrite.println("1");
                                            } else {
                                                pwrite.println("0");
                                            }
                                            pwrite.flush();
                                            break;
                                        case "lb":
                                            pressed = gamepad.left_bumper;
                                            if (pressed) {
                                                pwrite.println("1");
                                            } else {
                                                pwrite.println("0");
                                            }
                                            pwrite.flush();
                                            break;
                                        case "rb":
                                            pressed = gamepad.right_bumper;
                                            if (pressed) {
                                                pwrite.println("1");
                                            } else {
                                                pwrite.println("0");
                                            }
                                            pwrite.flush();
                                            break;
                                        case "lt":
                                            joyval = gamepad.left_trigger;
                                            pwrite.println(joyval);
                                            pwrite.flush();
                                            break;
                                        case "rt":
                                            joyval = gamepad.right_trigger;
                                            pwrite.println(joyval);
                                            pwrite.flush();
                                            break;
                                    }


                            }

                        }
                    }
                    sock.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }


        }
    }

    /*
    * Constructor
    */
    public PythonOp() {

    }

    /*
    * Code to run when the op mode is first enabled goes here
    * @see com.qualcomm.robotcore.eventloop.opmode.OpMode#start()
    */
    @Override
    public void start() {
        running = true;
        startPythonActivity();
        MyClientTask myClientTask = new MyClientTask("127.0.0.1",25658);
        myClientTask.start();
    }
    /*
    * This method will be called repeatedly in a loop
    * @see com.qualcomm.robotcore.eventloop.opmode.OpMode#loop()
    */
    @Override
    public void loop() {

    }

    /*
    * Code to run when the op mode is first disabled goes here
    * @see com.qualcomm.robotcore.eventloop.opmode.OpMode#stop()
    */
    @Override
    public void stop() {
        running = false;
    }
}

