package com.qualcomm.ftcrobotcontroller.opmodes;

import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.app.Activity;

import com.qualcomm.ftcrobotcontroller.FtcRobotControllerActivity;
import com.qualcomm.robotcore.eventloop.opmode.OpMode;
import com.qualcomm.robotcore.hardware.DcMotor;
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

/**
 * An empty op mode serving as a template for custom OpModes
 */
public class PythonOp extends OpMode {

    boolean running;

    class MyClientTask extends Thread {
        String ipaddress;
        int portnumber;
        Map<String,DcMotor> motors = new HashMap<String,DcMotor>();

        MyClientTask(String ip, int port) {
            ipaddress = ip;
            portnumber = port;
        }

        @Override
        public void run() {
            try {
                Socket sock = new Socket(ipaddress, portnumber);


                OutputStream ostream = sock.getOutputStream();
                PrintWriter pwrite = new PrintWriter(ostream, true);

                InputStream istream = sock.getInputStream();
                BufferedReader receiveRead = new BufferedReader(new InputStreamReader(istream));

                boolean keep = true;

                String sendMessage;
                String receiveMessage;
                while (keep) {
//                    sendMessage = "test";
//                    pwrite.println(sendMessage);
//                    pwrite.flush();
                    if ((receiveMessage = receiveRead.readLine()) != null) {
                        char[] charArray = receiveMessage.toCharArray();
                        String[] args = receiveMessage.split(",");
                        switch (charArray[0]) {
                            case 'A':
                                //Set motor
                                int power = new Integer(args[2]);
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
                                if (args[2] == "1") {
                                    motors.get(args[1]).setDirection(DcMotor.Direction.REVERSE);
                                }
                                break;
                        }

                    }
                }
                sock.close();
            } catch (UnknownHostException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
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

