package edu.msoe.smv.raspi;

import com.google.gson.GsonBuilder;

import java.util.Date;

/**
 * This class represents the state of the vehicle at a specific point in time
 *
 * @author matt
 */
public class DataNode {

	private final Date date;
	private final double rpm;
	private final double speed;

	public DataNode(double rpm, double speed) {
		this.rpm = rpm;
		this.speed = speed;
		this.date = new Date();
	}

	public Date getDate() {
		return date;
	}

	public double getRpm() {
		return rpm;
	}

	/**
	 * Returns a string representation of this node formatted in JSON.
	 * </p>
	 * Pretty printing is used, that is the resulting string spans multiple lines. For example: </p>
	 * <pre>{
	 *     "altitude": 5.0,
	 *     "batteryVoltage": 2.0,
	 *     "date": "Oct 25, 2014 2:04:23 PM",
	 *     "latitude": 3.0,
	 *     "longitude": 5.0,
	 *     "rpm": 1.0
	 * }</pre>
	 *
	 * @return a string representation of this node formatted in JSON
	 */
	@Override
	public String toString() {
		return new GsonBuilder().setPrettyPrinting().create().toJson(this);
	}

	/**
	 * Returns a string representation of this DataNode as comma-separated values.
	 * <p/>
	 * Example result: <pre>12345678,200,20</pre> where the first value is the Unix time, the second is the RPM, and
	 * the third is the speed.
	 *
	 * @return a string representation of this DataNode as comma-separated values
	 */
	public String toCSV() {
		return date.getTime() + "," + rpm + "," + speed;
	}
}
