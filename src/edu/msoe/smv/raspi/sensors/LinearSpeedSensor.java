package edu.msoe.smv.raspi.sensors;

public class LinearSpeedSensor extends DataCollector {
	/**
	 * The linear speed of this sensor in inches/second
	 */
	private double linearSpeed;
	/**
	 * The distance from the axis of rotational to the sensor in inches
	 */
	private double radius;
	/**
	 * The {@link edu.msoe.smv.raspi.sensors.RotationalSpeedSensor} this LinearSpeedSensor wraps.
	 * <p/>
	 * Whenever {@link #getLinearSpeed} or {@link #getValue} is called, {@link #computeLinearSpeed} is also called to
	 * update {@link #linearSpeed}
	 */
	private RotationalSpeedSensor rotationalSpeedSensor;

	/**
	 * Creates a linear speed sensor that
	 *
	 * @param pinNum                the pin number this sensor is connected to
	 * @param radius                radius of from the axis of rotation to this sensor (inches)
	 * @param rotationalSpeedSensor the rotational speed sensor this wraps
	 */
	public LinearSpeedSensor(int pinNum, double radius, RotationalSpeedSensor rotationalSpeedSensor) {
		super(pinNum);
		this.radius = radius;
		this.rotationalSpeedSensor = rotationalSpeedSensor;
	}

	/**
	 * Returns the linear speed of this sensor in miles per hour
	 *
	 * @return the linear speed of this sensor in miles per hour
	 */
	@Override
	public double getValue() {
		computeLinearSpeed();

		double result = this.linearSpeed;   // inches per second
		result *= 3600.0;                   // inches per hour
		result /= 12.0;                     // feet per hour
		result /= 5280.0;                   // miles per hour

		return result;
	}

	/**
	 * Computes and sets the linear speed.
	 */
	private void computeLinearSpeed() {
		this.linearSpeed = radius * rotationalSpeedSensor.getRotationalSpeed();
	}

	/**
	 * Returns the linear speed of this sensor in inches per second
	 *
	 * @return {@link #linearSpeed}
	 */
	public double getLinearSpeed() {
		computeLinearSpeed();

		return this.linearSpeed;
	}
}
