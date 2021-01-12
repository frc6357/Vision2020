import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.util.Base64;

public class UDPServer {
	
	public final static int SERVICE_PORT=5005;
	

	public static void main(String[] args) throws IOException{
		try {
			DatagramSocket sSocket = new DatagramSocket(SERVICE_PORT);
			// binds socket to specified port on computer
			
			byte[] rDataBuffer = new byte[1024];
			// memory allocated for packets to be read on the computer
			byte[] sDataBuffer = new byte[1024];
			// memory allocated to send packets from the computer
			boolean running = true;

			
			while(running) {
				
				DatagramPacket inputPacket = new DatagramPacket(rDataBuffer, rDataBuffer.length);
				// create Datagram packet with size equal to size of rDataBuffer
				System.out.println("Waiting for message....");
				
				sSocket.receive(inputPacket);
				// get the packet at the port defined by sSocket
				
				String rData = new String(inputPacket.getData());
				// get the data from the packet at the port defined by sSocket as a string
				System.out.println("Sent from the client: " + rData);
				
				
				/*
				System.out.println(Base64.getEncoder().encodeToString(inputPacket.getData()).contentEquals("end"));
				
				if (rData.equals("end")) {
					String ending = "ending";
					sDataBuffer = ending.getBytes();
					
					InetAddress sAddress = inputPacket.getAddress();
					int sPort = inputPacket.getPort();
					System.out.println(sPort + " " + sAddress);
					DatagramPacket outputPacket = new DatagramPacket(sDataBuffer, sDataBuffer.length, sAddress, sPort);
					
					outputPacket = new DatagramPacket(sDataBuffer, sDataBuffer.length, sAddress, sPort);
					
					sSocket.send(outputPacket);
					
					sSocket.close();
					System.exit(0);
					
				}
				*/
				
				// not a priority
				
				
				sDataBuffer = rData.toUpperCase().getBytes();
				
				
				InetAddress sAddress = inputPacket.getAddress();
				// gets ip address of the device that sent the packet
				int sPort = inputPacket.getPort();
				// gets port of the device that sent the packet
				System.out.println(sPort + " " + sAddress);
				DatagramPacket outputPacket = new DatagramPacket(sDataBuffer, sDataBuffer.length, sAddress, sPort);
				// creates new Datagram packet of size equal to size of sDatabuffer
				// creates Datagram packet to be sent to device that sent the inputPacket (sAddress sPort)
				
				sSocket.send(outputPacket);
				// sends packet from computer to the device that sent inputPacket 
				
				rDataBuffer = new byte[1024];
				// refreshes memory to empty
				
				
			}
		}
		catch (SocketException e) {
			e.printStackTrace();
		}

	}

}
