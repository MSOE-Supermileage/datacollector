package edu.msoe.smv;

import com.google.gson.Gson;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public enum VehicleAttributes {
	MP82(1, 20.0, 3), MP680(4, 20.0, 6), MP252(7, 20.0, 9);

	private double axleDiameter;
	private double engineShaftDiameter;
	private double tireDiameter;

	VehicleAttributes(double axleDiameter, double tireDiameter, double engineShaftDiameter) {
		this.axleDiameter = axleDiameter;
		this.tireDiameter = tireDiameter;
		this.engineShaftDiameter = engineShaftDiameter;
	}

	/**
	 * Creates a new VehicleAttribute based on the data in the specified JSON file.
	 * <p/>
	 * Recommended: Use Gson to create the JSON
	 *
	 * @param file the JSON file to build the vehicle from
	 */
	VehicleAttributes(File file) {
		Gson gson = new Gson();
		try {
			Scanner scan = new Scanner(file);
			String json = "";
			while(scan.hasNext()) json += scan.next();

			VehicleAttributes vehicle = gson.fromJson(json, this.getClass());
			this.axleDiameter = vehicle.getAxleDiam();
			this.engineShaftDiameter = vehicle.getEngineShaftDiam();
			this.tireDiameter = vehicle.getTireDiam();
		} catch(FileNotFoundException e) {
			e.printStackTrace();
			System.exit(-1);
		}
	}

	public double getAxleDiam() {
		return this.axleDiameter;
	}

	public double getEngineShaftDiam() {
		return this.engineShaftDiameter;
	}

	public double getTireDiam() {
		return this.tireDiameter;
	}
}
