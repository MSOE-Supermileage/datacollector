package edu.msoe.smv.raspi;

import com.google.gson.GsonBuilder;

/**
 * This class represents the state of the vehicle at a specific point in time
 *
 * @author matt
 */
public class DataNode {
	/**
	 * The UNIX epoch when this DataNode was created
	 */
	private final long unixTime;
	/**
	 * The rpm at this DataNode
	 */
	private final double rpm;
	/**
	 * The speed at this DataNode
	 */
	private final double speed;

	/**
	 * Constructs a new DataNode
	 * @param rpm the RPM at this DataNode
	 * @param speed the speed at this DataNode
	 */
	public DataNode(double rpm, double speed) {
		this.rpm = rpm;
		this.speed = speed;
		this.unixTime = System.currentTimeMillis();
	}

	/**
	 * Returns the UNIX epoch time when this DataNode was created
	 * @return the UNIX epoch time when this DataNode was created
	 */
	public long getUnixTime() {
		return unixTime;
	}

	/**
	 * Returns the RPM at this DataNode
	 * @return the RPM at this DataNode
	 */
	public double getRpm() {
		return rpm;
	}

	/**
	 * Returns the speed at this DataNode
	 * @return the speed at this DataNode
	 */
	public double getSpeed() {
		return speed;
	}

	/**
	 * Returns a string representation of this node formatted in JSON.
	 * </p>
	 * Pretty printing is used, that is the resulting string spans multiple lines. For example: </p>
	 * <pre>{
	 *     "altitude": 5.0,
	 *     "batteryVoltage": 2.0,
	 *     "unixTime": 1414263863,
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
		return unixTime + "," + rpm + "," + speed;
	}
}
