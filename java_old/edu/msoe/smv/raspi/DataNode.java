package edu.msoe.smv.raspi;

import com.google.gson.GsonBuilder;

/**
 * This class represents the state of the vehicle at a specific point in time
 *
 * @author matt
 */
public class DataNode {
	/**
	 * Counts the number of DataNodes created.
	 * <p/>
	 * This is used to track how far the vehicle has gone.
	 */
	private static long count = 0;
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
	 *
	 * @param rpm      the RPM at this DataNode
	 * @param speed    the speed at this DataNode
	 * @param realData false if this DataNode is a dummy DataNode
	 */
	public DataNode(double rpm, double speed, boolean realData) {
		this.rpm = rpm;
		this.speed = speed;
		this.unixTime = System.currentTimeMillis();

		if (realData) {
			count++;
		}
	}

	/**
	 * Returns the UNIX epoch time when this DataNode was created
	 *
	 * @return the UNIX epoch time when this DataNode was created
	 */
	public long getUnixTime() {
		return unixTime;
	}

	/**
	 * Returns the RPM at this DataNode
	 *
	 * @return the RPM at this DataNode
	 */
	public double getRpm() {
		return rpm;
	}

	/**
	 * Returns the speed at this DataNode
	 *
	 * @return the speed at this DataNode
	 */
	public double getSpeed() {
		return speed;
	}

	/**
	 * Returns a string representation of this node formatted in JSON. </p> Pretty printing is used, that is the
	 * resulting string spans multiple lines. For example: </p>
	 * <pre>{
	 *     "unixTime": 1414263863,
	 *     "rpm": 1.0,
	 *     "speed": 2.0,
	 *     "count": 23
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
	 * Example result: <pre>12345678,200,20,1</pre> where the first value is the Unix time, the second is the RPM, and
	 * the third is the speed, and the fourth is the count.
	 *
	 * @return a string representation of this DataNode as comma-separated values
	 */
	public String toCSV() {
		return unixTime + "," + rpm + "," + speed + "," + count;
	}
}
