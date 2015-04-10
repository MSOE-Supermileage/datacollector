package edu.msoe.smv.raspi;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.SocketAddress;
import java.net.SocketException;
import java.util.List;

public class AndroidServer implements Runnable {

	/**
	 * The default port to use for sending data.
	 */
	public static final int DEFAULT_PORT = 12100;
	/**
	 * How many milliseconds to wait before sending more data.
	 * <p/>
	 * Set to 33 milliseconds, or 1/30 seconds.
	 */
	public static final long SEND_INTERVAL = (long) ((1 / 30) * 1E3);

	/**
	 * The singleton instance of this class
	 */
	private static volatile AndroidServer instance;

	/**
	 * The list of {@link edu.msoe.smv.raspi.DataNode DataNodes} to send. It is recommended that Vector or another
	 * thread-safe implementation is used.
	 *
	 * @see java.util.Collections.SynchronizedList
	 * @see java.util.Vector
	 */
	private final List<DataNode> nodeList;
	/**
	 * The port used for sending data.
	 */
	private int port;
	/**
	 * Whether or not to run the server.
	 */
	private boolean runServer;
	/**
	 * The socket to send datagrams to and receive datagrams from.
	 */
	private DatagramSocket socket;

	/**
	 * Creates a server instance that will send the elements of {@code nodeList} over the specified port.
	 *
	 * @param nodeList the data to send
	 * @param port     the port to send data over
	 * @throws SocketException
	 */
	private AndroidServer(List<DataNode> nodeList, int port) throws SocketException {
		this.nodeList = nodeList;
		this.port = port;
		this.runServer = true;
		this.socket = new DatagramSocket(this.port);
	}

	/**
	 * Returns the singleton instance of this class using the specified List of DataNodes and the {@link
	 * #DEFAULT_PORT}.
	 *
	 * @param nodeList the data to send
	 * @return a singleton instance of this class
	 * @throws SocketException
	 */
	public static AndroidServer getInstance(List<DataNode> nodeList) throws SocketException {
		return getInstance(nodeList, DEFAULT_PORT);
	}

	/**
	 * Returns the singleton instance of this class using the specified List of DataNodes and port.
	 *
	 * @param nodeList the data to send
	 * @param port     the port to send data over
	 * @return a singleton instance of this class
	 * @throws SocketException
	 */
	public static AndroidServer getInstance(List<DataNode> nodeList, int port) throws SocketException {
		if (instance == null) {
			synchronized (AndroidServer.class) {
				if (instance == null) {
					instance = new AndroidServer(nodeList, port);
				}
			}
		}
		return instance;
	}

	/**
	 * Enables or disables the server.
	 * <p/>
	 * When {@code enable} is <tt>true</tt> the server continues to send data; when {@code enable} is <tt>false</tt> the
	 * server stops sending data.
	 *
	 * @param enable the state of the server
	 */
	public void enableServer(boolean enable) {
		this.runServer = enable;
	}

	/**
	 * Returns the port being used by this server.
	 *
	 * @return the port being used by this server
	 */
	public int getPort() {
		return port;
	}

	/**
	 * Returns the List of DataNodes being sent by this server
	 *
	 * @return the list of DataNodes being sent by this server
	 */
	public List<DataNode> getNodeList() {
		return nodeList;
	}

	/**
	 * When an object implementing interface {@code Runnable} is used to create a thread, starting the thread causes the
	 * object's {@code run} method to be called in that separately executing thread.
	 * <p/>
	 * The general contract of the method {@code run} is that it may take any action whatsoever.
	 *
	 * @see Thread#run()
	 */
	@Override
	public void run() {
		while (runServer) {
			try {
				// create a dummy buffer to store received data
				byte[] buf = new byte[256];
				DatagramPacket packet = new DatagramPacket(buf, buf.length);
				// NOTE This is blocking! It must receive some data to continue, so send the Pi data to get data.
				socket.receive(packet);

				if (nodeList.size() > 0) {
					// get the data to send
					synchronized (nodeList) {
						// lets stay away from IndexOutOfBoundsException, mmk?
						System.out.println("nodeList.size() = " + nodeList.size());
						DataNode dn = nodeList.remove(0);
						System.out.println("nodeList.size() = " + nodeList.size());
						buf = dn.toString().getBytes();
					}
				} else {
					// send negative values to tell the Android device to ignore this DataNode
					String data = new DataNode(-1, -1, false).toString();
					buf = data.getBytes();
				}

				// send the data
				SocketAddress address = packet.getSocketAddress();
				packet = new DatagramPacket(buf, buf.length, address);
				socket.send(packet);

				try {
					Thread.sleep(50);
				} catch (InterruptedException e) {
					System.err.println("Failed to sleep for " + SEND_INTERVAL + " ms. Continuing...");
				}
			} catch (IOException e) {
				System.err.println("An IOException occurred while send/receiving data. Shutting down server.");
				e.printStackTrace();
				runServer = false;
			}
		}
	}
}
