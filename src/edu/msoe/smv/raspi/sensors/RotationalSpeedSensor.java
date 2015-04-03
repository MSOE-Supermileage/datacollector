package edu.msoe.smv.raspi.sensors;

import com.pi4j.io.gpio.GpioFactory;
import com.pi4j.io.gpio.GpioPinDigitalInput;
import com.pi4j.io.gpio.PinState;
import com.pi4j.io.gpio.trigger.GpioCallbackTrigger;

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
				GpioFactory.getInstance().provisionDigitalInputPin(DataCollector.getRaspiPin(pinNum), "rotational speed sensor");
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
		double dt = Math.abs(System.currentTimeMillis() - lastInterrupt) / 1000.0;  // seconds

		this.rotationalSpeed = dTheta / dt;     // radians per second
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
	 * Returns the rotational speed of this sensor in revolutions per minute.
	 * <p/>
	 * Note that this will only show good data after {@link #computeRotationalSpeed()} has been called.
	 *
	 * @return the rotational speed of this sensor in revolutions per minute
	 */
	@Override
	public double getValue() {
		double result = this.rotationalSpeed;
		result *= 60.0;                        // radians per minute
		result /= 2.0 * Math.PI;               // revolutions per minute

		return result;
	}

	/**
	 * Returns the rotational speed of this sensor in radians per second
	 *
	 * @return {@link #rotationalSpeed}
	 */
	public double getRotationalSpeed() {
		return this.rotationalSpeed;
	}
}
