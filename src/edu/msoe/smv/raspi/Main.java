package edu.msoe.smv.raspi;

import com.pi4j.io.gpio.PinState;
import edu.msoe.smv.VehicleAttributes;
import edu.msoe.smv.raspi.sensors.RotationalSpeedSensor;

import java.net.SocketException;
import java.util.LinkedList;
import java.util.List;

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
		System.out.println("Chosen vehicle: " + vehicle);

		final List<DataNode> nodeList = new LinkedList<>();
		try {
			// init server
			Server server = Server.getInstance(nodeList);
			Thread serverThread = new Thread(server);
			server.enableServer(true);
			System.out.println("Made server");

			// init rotational speed sensor
			final RotationalSpeedSensor rotationalSpeedSensor = new RotationalSpeedSensor(7, PinState.HIGH, 1);
			rotationalSpeedSensor.setNodeList(nodeList);
			System.out.println("Made rotational speed sensor");

			// start threads
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
