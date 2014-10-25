package edu.msoe.smv.raspi;

import com.google.gson.GsonBuilder;

import java.util.Date;

/**
 * This class represents the state of the vehicle at a specific point in time
 *
 * @author matt
 */
public class DataNode {

	private final double altitude;
	private final double batteryVoltage;
	private final Date date;
	private final double latitude;
	private final double longitude;
	private final double rpm;

	public DataNode(double rpm, double batteryVoltage, double latitude, double longitude, double altitude) {
		this.rpm = rpm;
		this.batteryVoltage = batteryVoltage;
		this.latitude = latitude;
		this.longitude = longitude;
		this.altitude = altitude;

		this.date = new Date();
	}

	public double getAltitude() {
		return altitude;
	}

	public double getBatteryVoltage() {
		return batteryVoltage;
	}

	public Date getDate() {
		return date;
	}

	public double getLatitude() {
		return latitude;
	}

	public double getLongitude() {
		return longitude;
	}

	public double getRpm() {
		return rpm;
	}

	/**
	 * Returns a string representation of this node formatted in JSON.
	 * </p>
	 * Pretty printing is used, that is the resulting string spans multiple lines. For example: </p>
	 * <code>{
	 *     "altitude": 5.0,
	 *     "batteryVoltage": 2.0,
	 *     "date": "Oct 25, 2014 2:04:23 PM",
	 *     "latitude": 3.0,
	 *     "longitude": 5.0,
	 *     "rpm": 1.0
	 * }</code>
	 *
	 * @return a string representation of this node formatted in JSON
	 */
	@Override
	public String toString() {
		return new GsonBuilder().setPrettyPrinting().create().toJson(this);
	}
}
