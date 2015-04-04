package edu.msoe.smv.raspi;

import java.io.*;

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
	 * @throws IOException if <tt>file</tt> could not be created
	 * @throws FileWritableException if <tt>file</tt> is not writable
	 */
	public DataLogger(File file) throws IOException {
		if (file == null) {
			throw new IllegalArgumentException("file cannot be null");
		}
		if (!file.exists()) {
			file.createNewFile();
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
