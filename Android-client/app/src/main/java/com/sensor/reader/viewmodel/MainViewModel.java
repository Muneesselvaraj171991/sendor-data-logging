package com.sensor.reader.viewmodel;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;
import com.sensor.reader.network.RemoteCall;

public class MainViewModel extends ViewModel {
    private final RemoteCall mRemoteCall = RemoteCall.getRemoteCallInstance();
    private final MutableLiveData<String> mSensorDataLivedata = new MutableLiveData<>();

    public void init() {
        mRemoteCall.getSensorData(value ->{
        mSensorDataLivedata.postValue(value);});
    }
    public LiveData<String> getSendorLiveData() {
        return mSensorDataLivedata;
    }

}
