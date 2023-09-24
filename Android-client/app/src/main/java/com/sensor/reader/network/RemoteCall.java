package com.sensor.reader.network;

import java.io.BufferedInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

public class RemoteCall {
    //http://10.0.2.2 is treated as localhost in android emulator, If you are using android phone use , do not forget to assign relevant hosting ip address.
    private static final String URL ="http://10.0.2.2:5000/sensor_data";
    private java.net.URL mUrl;
    private static RemoteCall sRemoteCall;
    private RemoteCall()  {

        try {
            mUrl = new URL(URL);
        } catch (MalformedURLException e) {
            e.printStackTrace();
        }
    }

    public static synchronized  RemoteCall getRemoteCallInstance() {
        if(sRemoteCall == null) {
            sRemoteCall = new RemoteCall();
        }
        return sRemoteCall;
    }

    public void getSensorData(Result result) {
        new Thread()
        {
            public void run() {
                try {
                    HttpURLConnection urlConnection = (HttpURLConnection) mUrl.openConnection();
                    InputStream in = new BufferedInputStream(urlConnection.getInputStream());
                    result.onResponse(readStream(in));
                } catch (IOException exception) {
                    exception.printStackTrace();
                    result.onResponse("Unable to connect sensor generation server");
                }
            }
        }.start();


    }

    private String readStream(InputStream is) throws IOException {
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        int readBuffer = is.read();
        while(readBuffer != -1) {
            outputStream.write(readBuffer);
            readBuffer = is.read();
        }
        return outputStream.toString();

    }

    public interface Result {
        void onResponse(String sensorData);

    }
}
