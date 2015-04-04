package edu.msoe.smv.raspi;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.PrintWriter;

/**
 * Logs {@link DataNode DataNodes} to a file.
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

	/**
	 * Constructs a new DataLogger that logs to <tt>file</tt>
	 *
	 * @param file the file to log to
	 * @throws FileNotFoundException
	 * @throws FileWritableException if <tt>file</tt> is not writable
	 */
	public DataLogger(File file) throws FileNotFoundException {
		if (file == null) {
			throw new IllegalArgumentException("file cannot be null");
		}
		if (!file.canWrite() || !file.setWritable(true)) {
			throw new FileWritableException("log file could not be set writable");
		}

		this.logFile = file;
		this.writer = new PrintWriter(new FileOutputStream(logFile, true));
		// print header line to log file
		this.writer.println("Milliseconds,RPM,MPH");
	}

	/**
	 * Prints a DataNode's CSV to {@link #logFile}
	 *
	 * @param dataNode the DataNode to print
	 */
	public void log(DataNode dataNode) {
		writer.println(dataNode.toCSV());
		writer.flush();
	}

}
