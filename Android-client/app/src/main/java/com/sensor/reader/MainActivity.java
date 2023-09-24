package com.sensor.reader;

import androidx.appcompat.app.AppCompatActivity;
import androidx.lifecycle.ViewModelProvider;

import android.os.Bundle;
import android.widget.TextView;
import android.widget.Toolbar;

import com.sensor.reader.viewmodel.MainViewModel;

import java.util.Objects;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        MainViewModel viewModel = new ViewModelProvider(this).get(MainViewModel.class);
        viewModel.init();
        Objects.requireNonNull(getSupportActionBar()).setTitle("Sensor data in JSON");

        TextView jsonText = findViewById(R.id.sensor_text);
        viewModel.getSendorLiveData().observe(this, sensorData -> {
            if(!"[]".equals(sensorData)) {
                jsonText.setText(sensorData);
            } else {
                jsonText.setText("Sensor server does not have any logs as of now ");
            }
        });
    }
}