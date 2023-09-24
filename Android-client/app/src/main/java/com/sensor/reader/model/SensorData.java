package com.sensor.reader.model;

import android.os.Parcel;
import android.os.Parcelable;

import androidx.annotation.NonNull;

import java.lang.String;
import java.math.BigDecimal;

public class SensorData implements Parcelable {
  private String name;

  private BigDecimal temperature;

  private BigDecimal humidity;

  private String timestamp;

  protected SensorData(Parcel in) {
    name = in.readString();
    timestamp = in.readString();
  }

  public static final Creator<SensorData> CREATOR = new Creator<SensorData>() {
    @Override
    public SensorData createFromParcel(Parcel in) {
      return new SensorData(in);
    }

    @Override
    public SensorData[] newArray(int size) {
      return new SensorData[size];
    }
  };

  public String getName() {
    return this.name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public BigDecimal getTemperature() {
    return this.temperature;
  }

  public void setTemperature(BigDecimal temperature) {
    this.temperature = temperature;
  }

  public BigDecimal getHumidity() {
    return this.humidity;
  }

  public void setHumidity(BigDecimal humidity) {
    this.humidity = humidity;
  }

  public String getTimestamp() {
    return this.timestamp;
  }

  public void setTimestamp(String timestamp) {
    this.timestamp = timestamp;
  }

  @Override
  public int describeContents() {
    return 0;
  }

  @Override
  public void writeToParcel(@NonNull Parcel dest, int flags) {
    dest.writeString(name);
    dest.writeString(timestamp);
  }
}
