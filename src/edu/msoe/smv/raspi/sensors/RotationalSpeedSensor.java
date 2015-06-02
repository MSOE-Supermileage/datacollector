package edu.msoe.smv.raspi.sensors;

import com.pi4j.io.gpio.GpioFactory;
import com.pi4j.io.gpio.GpioPinDigitalInput;
import com.pi4j.io.gpio.PinPullResistance;
import com.pi4j.io.gpio.PinState;
import com.pi4j.io.gpio.trigger.GpioCallbackTrigger;
import edu.msoe.smv.VehicleAttributes;
import edu.msoe.smv.raspi.AndroidServer;
import edu.msoe.smv.raspi.DataNode;

import java.net.SocketException;
import java.util.List;
import java.util.concurrent.Callable;

/**
 * TODO
 */
public class RotationalSpeedSensor extends DataCollector {
	/**
	 * The UNIX epoch time (milliseconds since 1970-01-01T00:00:00Z) of the previous interrupt
	 */
	private long lastInterrupt;
	/**
	 * TODO
	 */
	private long currentInterrupt;
	/**
	 * The number of possible interruptions per complete rotational of the sensor.
	 * <p/>
	 * For instance, if this sensor is collecting data from a hall-effect sensor on something that is spinning, and the
	 * hall-effect sensor passes a magnet three times per rotation, <tt>numberOfInterruptsPerRotation</tt> should be set
	 * to three.
	 */
	private int numberOfInterruptsPerRotation;
	/**
	 * The rotation speed of this sensor in radians/second
	 */
	private double rotationalSpeed;
	/**
	 * The linear speed of this sensor in miles/hour
	 */
	private double linearSpeed;
	private List<DataNode> nodeList;
	private List<DataNode> androidNodeList;

	/**
	 * TODO
	 *
	 * @param pinNum                        the pin number this sensor is connected to
	 * @param pinState                      the state of the pin when the rotational speed should be calculated
	 * @param numberOfInterruptsPerRotation the total number of possible interrupts this sensor may receive per complete
	 *                                      rotation
	 */
	public RotationalSpeedSensor(int pinNum, PinState pinState, int numberOfInterruptsPerRotation) {
		super(pinNum);
		this.numberOfInterruptsPerRotation = numberOfInterruptsPerRotation;
		this.lastInterrupt = System.currentTimeMillis();

		final GpioPinDigitalInput rotSpeedSensor =
				GpioFactory.getInstance().provisionDigitalInputPin(DataCollector.getRaspiPin(pinNum), PinPullResistance.PULL_UP);
		rotSpeedSensor.setDebounce(20);
		rotSpeedSensor.addTrigger(new GpioCallbackTrigger(pinState, new Callable<Void>() {
			@Override
			public Void call() throws Exception {
				computeRotationalSpeed();
				return null;
			}
		}));
	}

	/**
	 * Computes and sets the rotational speed.
	 * <p/>
	 * NOTE: This method should only be called when there is a state change on the pin
	 */
	private void computeRotationalSpeed() {
		double dTheta = (2.0 * Math.PI) / numberOfInterruptsPerRotation;            // radians
		this.currentInterrupt = System.currentTimeMillis();
		double dt = Math.abs(currentInterrupt - lastInterrupt) / 1000.0;            // seconds

		this.rotationalSpeed = dTheta / dt;     // radians per second

		double rpm = getValue();
		double speed = rpm * (VehicleAttributes.MP82.getTireDiam() / 2);    // inches per second
		speed *= 3600.0;                                                    // inches per hour
		speed /= 63360.0;                                                   // miles per hour

		double circumference = 2 * Math.PI * (20.0 / 2.0) / 12.0 / 5280.0;  // miles
		this.linearSpeed = circumference / dt * 3600.0; // mph

		DataNode dataNode = new DataNode(rpm, this.linearSpeed, true);

		if (nodeList != null) {
			nodeList.add(dataNode);
		}
		if (androidNodeList != null) {
			androidNodeList.add(dataNode);
//			try {
//				AndroidServer.getInstance(androidNodeList).setCurrentNode(dataNode);
//			} catch (SocketException e) {
//				System.err.println("Failed to set current DataNode for AndroidServer");
//				System.err.println(e.getMessage());
//			}
		}
		this.lastInterrupt = currentInterrupt;
	}

	/**
	 * Returns the rotational speed of this sensor in revolutions per minute.
	 * <p/>
	 * Note that this will only show good data after {@link #computeRotationalSpeed()} has been called.
	 *
	 * @return the rotational speed of this sensor in revolutions per minute
	 */
	@Override
	public double getValue() {
		double result = this.rotationalSpeed;   // radians per second
		result *= 60.0;                         // radians per minute
		result /= (2.0 * Math.PI);              // revolutions per minute

		return result;
	}

	/**
	 * TODO
	 *
	 * @param time
	 * @return
	 */
	public double getSmoothSpeed(long time) {
		double smoothSpeed;
		if (lastInterrupt - currentInterrupt < time - lastInterrupt) {
			smoothSpeed = getSpeed(lastInterrupt, time);
		} else {
			smoothSpeed = getSpeed(lastInterrupt, currentInterrupt);
		}
		return smoothSpeed;
	}

	private double getSpeed(long time1, long time2) {
		double circumference = 2.0 * Math.PI * (20.0 / 2.0) / 12.0 / 5280.0;  // miles
		circumference /= 2;
		double dt = Math.abs(time1 - time2) / 1000.0 / 3600.0;  // hours
		return circumference / dt;
	}

	/**
	 * Returns the number of possible interrupts per rotation
	 *
	 * @return the number of possible interrupts per rotation
	 */
	public int getNumberOfInterruptsPerRotation() {
		return this.numberOfInterruptsPerRotation;
	}

	/**
	 * Returns the rotational speed of this sensor in radians per second
	 *
	 * @return {@link #rotationalSpeed}
	 */
	public double getRotationalSpeed() {
		return this.rotationalSpeed;
	}

	public void setNodeList(List<DataNode> list) {
		this.nodeList = list;
	}

	public void setAndroidNodeList(List<DataNode> list) {
		this.androidNodeList = list;
	}
}
