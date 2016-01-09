package edu.msoe.smv.raspi;

import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;

/**
 * Created by matt on 4/4/15.
 */
public class LoggingServer implements Runnable {
	private static volatile LoggingServer instance;
	private final List<DataNode> nodeList;
	private boolean runServer;
	private DataLogger dataLogger;

	private LoggingServer(List<DataNode> list) {
		this.nodeList = list;
		try {
			SimpleDateFormat simpleDateFormat = new SimpleDateFormat("MM-dd_HH.mm.ss");
			this.dataLogger = new DataLogger(new File("/home/pi/daq_" + simpleDateFormat.format(new Date()) + ".log"));
		} catch (IOException e) {
			e.printStackTrace();
			System.out.println("Encountered an exception when creating the data logger.");
			System.out.println("Data will NOT be logged to a file.");
			this.dataLogger = null;
		}
	}

	public static LoggingServer getInstance(List<DataNode> nodeList) {
		if (instance == null) {
			synchronized (LoggingServer.class) {
				if (instance == null) {
					instance = new LoggingServer(nodeList);
				}
			}
		}

		return instance;
	}

	public void enableServer(boolean enable) {
		this.runServer = enable;
	}

	@Override
	public void run() {
		while (runServer) {
			if (nodeList.size() > 0) {
				DataNode dn;
				synchronized (nodeList) {
					dn = nodeList.remove(0);
				}
				if (dataLogger != null) {
					dataLogger.log(dn);
				}
			}
		}
	}
}
