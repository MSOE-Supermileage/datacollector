package edu.msoe.smv.raspi;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;

/**
 * TODO
 *
 * @author matt
 */
public class DataLogger {

	/**
	 * The file to log to
	 */
	private File logFile;
	/**
	 * The PrintWriter used for printing
	 */
	private PrintWriter writer;

	public DataLogger(File file) throws FileNotFoundException {
		if (file == null) {
			throw new IllegalArgumentException("file cannot be null");
		} else if (!file.canWrite() || !file.setWritable(true)) {
			throw new FileWritableException("log file could not be set writable");
		}

		this.logFile = file;
		this.writer = new PrintWriter(this.logFile);
	}

	/**
	 * Prints a DataNode's CSV to {@link #logFile}
	 *
	 * @param dataNode the DataNode to print
	 */
	public void log(DataNode dataNode) {
		writer.println(dataNode.toCSV());
	}

}
