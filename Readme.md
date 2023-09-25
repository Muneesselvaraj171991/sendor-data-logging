# Seson-data-logging

 The idea behind this task is to create a json log file from sensor simulator. Simulator produces data in binary, As an user It is us to parse and covert it as Json log file.

There can be a diffrent way to do this, But I have chosen to use PULL based RESTAPI, with that many clients be it Android , ios , we client and curl can communicate with server to get log files as stated below.

## Server-Client flow
![sensorserverclient](https://github.com/Muneesselvaraj171991/sendor-data-logging/assets/38101471/9a3ab628-c777-4653-a745-640875b92aab)
### Python server(codesource: sensor-data-logging/sensor-server)
For RESTAPI , I am using Flask framwork with a get method called "/sensor_data". Server is responsible for running **sendor_data** simulator to receive stdio and storing it in a class for json generation when api call is made. I am managing simulation running in a seperate thread, just not to block main thread. As you know simulation producess binary data atmost forever, so when user call the api I am parsing partially colleced data and covert it as json to send it to caller.

### Android Client(code: sensor-data-logging/Android-client)
 I choose Android as a client to demo the server-client flow. Made an app to connect to sensor data generation server, whenever app launches it fetch data from server and display json data to user. As data grows user can scroll as well.

### Result from my experiment.
I was able to successfully setup both server and client and see the data produces from sensor simulation. you can see the below screen for proofing.
![Android_client_for_sensor_data](https://github.com/Muneesselvaraj171991/sendor-data-logging/assets/38101471/f1fd34bd-acc0-4464-a710-38ee12aac340)

## How to Setup and Run applications.
I am using Windows as host, below prerequisites are intented for Windows machine.
 
### Prerequisite
Python, Android studio, pip install flask for RESTAPI.

### Run
**To start server:** python .\sensor-server\SensorDataServer.py
**Client:** Import app from sensor-data-logging/Android-client in Android studio and launch it in emulator.

### Limitations.
I have tested in web browser and Android emulator, If you are running in Android mobile, make sure you point to correct URL in RemoteCall.java class.

## Improvements
I am thinking Server-client communication can be a **Push-Based** instead of pull-based. Since this is the assignment I may miss safe-fail stuffs in source. 

## Referencess 
https://www.geeksforgeeks.org/flask-creating-first-simple-application/
https://docs.python.org/3/library/subprocess.html
 
