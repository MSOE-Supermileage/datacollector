package edu.msoe.smv.raspi;

import com.pi4j.io.gpio.*;
import com.pi4j.io.gpio.trigger.GpioCallbackTrigger;
import com.pi4j.io.gpio.trigger.GpioSyncStateTrigger;
import com.pi4j.wiringpi.Gpio;
import edu.msoe.smv.VehicleAttributes;
import edu.msoe.smv.raspi.sensors.DataCollector;
import edu.msoe.smv.raspi.sensors.RotationalSpeedSensor;

import java.net.SocketException;
import java.util.Collections;
import java.util.LinkedList;
import java.util.List;
import java.util.concurrent.Callable;

/**
 * Created by matt on 3/21/15.
 */
public class Main {
	/**
	 * TODO
	 */
	private static VehicleAttributes vehicle;

	public static void main(String[] args) {
		// set VehicleAttributes vehicle
		if (args.length > 0) {
			setVehicle(args[0]);
		} else {
			System.out.println("You must specify which vehicle this is being run on.");
			System.out.println("For example:");
			System.out.println("\tsudo java -jar Raspberry_Pi.jar MP82");
			System.exit(1);
		}
		System.out.println(vehicle);
		try {
			Thread.sleep(1000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}

		// Run things
		final List<DataNode> nodeList = new LinkedList<DataNode>();
		try {
			Server server = Server.getInstance(nodeList);
			System.out.println("Made server");

			GpioController gpio = GpioFactory.getInstance();

			/*GpioPinDigitalInput counterGpio =
					gpio.provisionDigitalInputPin(RaspiPin.GPIO_07, PinPullResistance.PULL_UP);
			counterGpio.addTrigger(new GpioCallbackTrigger(PinState.HIGH, new Callable<Void>() {
				@Override
				public Void call() throws Exception {
					System.out.println("I found the magnet!");
					return null;
				}
			}));*/

//			final GpioPinDigitalOutput ledOut = gpio.provisionDigitalOutputPin(RaspiPin.GPIO_00, PinState.LOW);
//			final GpioPinDigitalInput foo = gpio.provisionDigitalInputPin(RaspiPin.GPIO_07, PinPullResistance.PULL_DOWN);
//			foo.addTrigger(new GpioSyncStateTrigger(ledOut));

			final RotationalSpeedSensor rotationalSpeedSensor = new RotationalSpeedSensor(7, PinState.HIGH, 1);
			rotationalSpeedSensor.setNodeList(nodeList);
			System.out.println("Made rot speed sensor");
			/*Thread getDatas = new Thread(new Runnable() {
				@Override
				public void run() {
					double tireDiam = vehicle.getTireDiam();
					while (true) {
						double foo = rotationalSpeedSensor.getValue();
						foo = Math.random();
						System.out.println("got omega value");
						DataNode dn = new DataNode(foo, tireDiam * foo);
						nodeList.add(dn);
					}
				}
			});
			System.out.println("Made data thread");*/

			Thread serverThread = new Thread(server);
			server.enableServer(true);
//			getDatas.start();
//			System.out.println("Started data thread");
			serverThread.start();
			System.out.println("Started server thread");
		} catch (SocketException e) {
			e.printStackTrace();
		}
	}

	/**
	 * Sets {@link #vehicle} to the correct {@link VehicleAttributes} enum.
	 * <p/>
	 * {@code vehicleName} should be the name of the vehicle that this is running on, for example "MP82", "MP680", or
	 * "MP252".
	 *
	 * @param vehicleName the name of the vehicle
	 */
	private static void setVehicle(String vehicleName) {
		if (vehicleName.contains("82")) {
			vehicle = VehicleAttributes.MP82;
		} else if (vehicleName.contains("680")) {
			vehicle = VehicleAttributes.MP680;
		} else {
			vehicle = VehicleAttributes.MP252;
		}
	}
}
