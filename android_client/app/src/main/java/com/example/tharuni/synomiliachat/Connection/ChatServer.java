//////package com.example.tharuni.synomiliachat.Connection;
////////
//////import java.net.ServerSocket;
////////
/////////**
//////// * Created by tharuni on 28/03/2017.
//////// */
////////
//////import java.net.*;
//////import java.io.*;
//////import java.io.BufferedReader;
//////import java.io.IOException;
//////import java.io.InputStreamReader;
//////import java.io.PrintWriter;
//////import java.net.ServerSocket;
//////import java.net.Socket;
//////import java.util.ArrayList;
//////
//////public class ChatServer {
////////
////////
/////////*
//////// * To change this license header, choose License Headers in Project Properties.
//////// * To change this template file, choose Tools | Templates
//////// * and open the template in the editor.
//////// */
////////
/////////**
//////// *
//////// * @author tharuni
//////// */
////////
////////
////////    /**
////////     * A multithreaded chat room server.  When a client connects the
////////     * server requests a screen name by sending the client the
////////     * text "SUBMITNAME", and keeps requesting a name until
////////     * a unique one is received.  After a client submits a unique
////////     * name, the server acknowledges with "NAMEACCEPTED".  Then
////////     * all messages from that client will be broadcast to all other
////////     * clients that have submitted a unique screen name.  The
////////     * broadcast messages are prefixed with "MESSAGE ".
////////     *
////////     */
////////
////////        /**
////////         * The port that the server listens on.
////////         */
////////        private static final int PORT = 8080;
////////
////////        /**
////////         * The set of all names of clients in the chat room.  Maintained
////////         * so that we can check that new clients are not registering name
////////         * already in use.
////////         */
////////        private static ArrayList<String> names = new ArrayList<String>();
////////
////////        /**
////////         * The set of all the print writers for all the clients.  This
////////         * set is kept so we can easily broadcast messages.
////////         */
////////        private static ArrayList<PrintWriter> writers = new ArrayList<PrintWriter>();
////////
////////        /**
////////         * The appplication main method, which just listens on a port and
////////         * spawns handler threads.
////////         */
////////        public static void main(String[] args) throws Exception {
////////            System.out.println("The chat server is running.");
////////            ServerSocket listener = new ServerSocket(PORT);
////////            try {
////////                while (true) {
////////                    new Handler(listener.accept()).start();
////////                }
////////            } finally {
////////                listener.close();
////////            }
////////        }
////////
////////        /**
////////         * A handler thread class.  Handlers are spawned from the listening
////////         * loop and are responsible for a dealing with a single client
////////         * and broadcasting its messages.
////////         */
////////        private static class Handler extends Thread {
//////        private static final int PORT = 8080;
//////        private static ArrayList<String> names = new ArrayList<String>();
//////        private static ArrayList<PrintWriter> writers = new ArrayList<PrintWriter>();
//////
//////
//////            private String name;
//////            private Socket socket;
//////            private BufferedReader in;
//////            private PrintWriter out;
//////
//////            /**
//////             * Constructs a handler thread, squirreling away the socket.
//////             * All the interesting work is done in the run method.
//////             */
//////            public ChatServer() {
//////                this.socket = socket;
//////               // ChatServer cs = new ChatServer().start();
//////            }
//////
//////    public void start() {
////////        System.out.println("testChat server started on port "
////////                + PORT_NUMBER + "!");
//////        try {
//////           ServerSocket s = new ServerSocket(PORT);
////////            for (;;) {
//////                Socket incoming = s.accept();
//////                new ChatServer().start();
////////            }
//////        } catch (Exception e) {
//////            e.printStackTrace();
//////        }
//////        System.out.println("testChat server stopped.");
//////    }
//////            /**
//////             * Services this thread's client by repeatedly requesting a
//////             * screen name until a unique one has been submitted, then
//////             * acknowledges the name and registers the output stream for
//////             * the client in a global set, then repeatedly gets inputs and
//////             * broadcasts them.
//////             */
//////            public void run() {
//////                try {
//////
//////                    // Create character streams for the socket.
//////                    in = new BufferedReader(new InputStreamReader(
//////                            socket.getInputStream()));
//////                    out = new PrintWriter(socket.getOutputStream(), true);
//////
//////                    // Request a name from this client.  Keep requesting until
//////                    // a name is submitted that is not already used.  Note that
//////                    // checking for the existence of a name and adding the name
//////                    // must be done while locking the set of names.
////////                    while (true) {
////////                        out.println("SUBMITNAME");
////////                        name = in.readLine();
////////                        if (name == null) {
////////                            return;
////////                        }
////////                        synchronized (names) {
////////                            if (!names.contains(name)) {
////////                                names.add(name);
////////                                break;
////////                            }
////////                        }
////////                    }
////////
////////                    // Now that a successful name has been chosen, add the
////////                    // socket's print writer to the set of all writers so
////////                    // this client can receive broadcast messages.
////////                    out.println("NAMEACCEPTED");
////////                    writers.add(out);
//////
//////                    // Accept messages from this client and broadcast them.
//////                    // Ignore other clients that cannot be broadcasted to.
//////                    while (true) {
//////                        String input = in.readLine();
//////                        if (input == null) {
//////                            return;
//////                        }
//////                        for (PrintWriter writer : writers) {
//////                            writer.println("MESSAGE " + name + ": " + input);
//////                        }
//////                    }
//////                } catch (IOException e) {
//////                    System.out.println(e);
//////
//////
//////                } finally {
//////                    // This client is going down!  Remove its name and its print
//////                    // writer from the sets, and close its socket.
//////                    if (name != null) {
//////                        names.remove(name);
//////                    }
//////                    if (out != null) {
//////                        writers.remove(out);
//////                    }
//////                    try {
//////                        socket.close();
//////                    } catch (IOException e) {
//////                    }
//////                }
//////            }
//////        }
//////
//////
////////
//////////
////////package com.example.tharuni.synomiliachat.Connection;
////////// $Id: ChatServer.java,v 1.3 2012/02/19 06:12:34 cheon Exp $
////////
////////import java.io.*;
////////import java.net.*;
////////import java.util.*;
////////
////////
////////public class ChatServer {
////////
////////    private static final String USAGE = "Usage: java ChatServer";
////////
////////    /** Default port number on which this server to be run. */
////////    private static final int PORT_NUMBER = 8080;
////////
////////    /** List of print writers associated with current clients,
////////     * one for each. */
////////    private List<PrintWriter> clients;
////////
////////    /** Creates a new server. */
////////    public ChatServer() {
////////        clients = new LinkedList<PrintWriter>();
////////    }
////////
////////    /** Starts the server. */
////////    public void start() {
////////        System.out.println("testChat server started on port "
////////                + PORT_NUMBER + "!");
////////        try {
////////            ServerSocket s = new ServerSocket(PORT_NUMBER);
////////            for (;;) {
////////                Socket incoming = s.accept();
////////                new ClientHandler(incoming).start();
////////            }
////////        } catch (Exception e) {
////////            e.printStackTrace();
////////        }
////////        System.out.println("testChat server stopped.");
////////    }
////////
////////    /** Adds a new client identified by the given print writer. */
////////    private void addClient(PrintWriter out) {
////////        synchronized(clients) {
////////            clients.add(out);
////////        }
////////    }
////////
////////    /** Adds the client with given print writer. */
////////    private void removeClient(PrintWriter out) {
////////        synchronized(clients) {
////////            clients.remove(out);
////////        }
////////    }
////////
////////    /** Broadcasts the given text to all clients. */
////////    private void broadcast(String msg) {
////////        for (PrintWriter out: clients) {
////////            out.println(msg);
////////            out.flush();
////////        }
////////    }
////////
////////    public static void main(String[] args) {
////////        if (args.length > 0) {
////////            System.out.println(USAGE);
////////            System.exit(-1);
////////        }
////////        new ChatServer().start();
////////    }
////////
////////    /** A thread to serve a client. This class receive messages from a
////////     * client and broadcasts them to all clients including the message
////////     * sender. */
////////    public class ClientHandler extends Thread {
////////
////////        /** Socket to read client messages. */
////////        private Socket incoming;
////////
////////        /** Creates a hander to serve the client on the given socket. */
////////        public ClientHandler(Socket incoming) {
////////            this.incoming = incoming;
////////        }
////////
////////        /** Starts receiving and broadcasting messages. */
////////        public void run() {
////////            PrintWriter out = null;
////////            try {
////////                out = new PrintWriter(
////////                        new OutputStreamWriter(incoming.getOutputStream()));
////////
////////                // inform the server of this new client
////////                ChatServer.this.addClient(out);
////////
////////                out.print("test de chat ");
////////                out.println("tape BYE pour exit.");
////////                out.flush();
////////
////////                BufferedReader in
////////                        = new BufferedReader(
////////                        new InputStreamReader(incoming.getInputStream()));
////////                for (;;) {
////////                    String msg = in.readLine();
////////                    if (msg == null) {
////////                        break;
////////                    } else {
////////                        if (msg.trim().equals("BYE"))
////////                            break;
////////                        System.out.println("Received: " + msg);
////////                        // broadcast the receive message
////////                        ChatServer.this.broadcast(msg);
////////                    }
////////                }
////////                incoming.close();
////////                ChatServer.this.removeClient(out);
////////            } catch (Exception e) {
////////                if (out != null) {
////////                    ChatServer.this.removeClient(out);
////////                }
////////                e.printStackTrace();
////////            }
////////        }
////////    }
////////}
////////
////////package com.example.tharuni.synomiliachat.Connection;
////////
////////import java.net.ServerSocket;
////////
/////////**
//////// * Created by tharuni on 28/03/2017.
//////// */
////////
////////        import java.net.*;
////////        import java.io.*;
////////        import java.io.BufferedReader;
////////        import java.io.IOException;
////////        import java.io.InputStreamReader;
////////        import java.io.PrintWriter;
////////        import java.net.ServerSocket;
////////        import java.net.Socket;
////////        import java.util.ArrayList;
////////
////////public class ChatServer {
////////
////////
/////////*
//////// * To change this license header, choose License Headers in Project Properties.
//////// * To change this template file, choose Tools | Templates
//////// * and open the template in the editor.
//////// */
////////
/////////**
//////// *
//////// * @author tharuni
//////// */
////////
////////
////////    /**
////////     * A multithreaded chat room server.  When a client connects the
////////     * server requests a screen name by sending the client the
////////     * text "SUBMITNAME", and keeps requesting a name until
////////     * a unique one is received.  After a client submits a unique
////////     * name, the server acknowledges with "NAMEACCEPTED".  Then
////////     * all messages from that client will be broadcast to all other
////////     * clients that have submitted a unique screen name.  The
////////     * broadcast messages are prefixed with "MESSAGE ".
////////     *
////////     */
////////
////////    /**
////////     * The port that the server listens on.
////////     */
////////    private static final int PORT = 8080;
////////
////////    /**
////////     * The set of all names of clients in the chat room.  Maintained
////////     * so that we can check that new clients are not registering name
////////     * already in use.
////////     */
////////    private static ArrayList<String> names = new ArrayList<String>();
////////
////////    /**
////////     * The set of all the print writers for all the clients.  This
////////     * set is kept so we can easily broadcast messages.
////////     */
////////    private static ArrayList<PrintWriter> writers = new ArrayList<PrintWriter>();
////////
////////    /**
////////     * The appplication main method, which just listens on a port and
////////     * spawns handler threads.
////////     */
//////////    public static void main(String[] args) throws Exception {
//////////        System.out.println("The chat server is running.");
//////////        ServerSocket listener = new ServerSocket(PORT);
//////////        try {
//////////            while (true) {
//////////                new Handler(listener.accept()).start();
//////////            }
//////////        } finally {
//////////            listener.close();
//////////        }
//////////    }
////////
/////////**
//////// * A handler thread class.  Handlers are spawned from the listening
//////// * loop and are responsible for a dealing with a single client
//////// * and broadcasting its messages.
//////// */
////
////
////
////package com.example.tharuni.synomiliachat.Connection;
////
////import java.io.BufferedReader;
////import java.io.IOException;
////import java.io.InputStreamReader;
////import java.io.OutputStreamWriter;
////import java.io.PrintWriter;
////import java.net.ServerSocket;
////import java.net.Socket;
////import java.text.SimpleDateFormat;
////import java.util.Calendar;
////
////
////public class ChatServer {
////
////    ServerSocket myServerSocket;
////    boolean ServerOn = true;
////
////
////    public ChatServer()
////    {
////        try
////        {
////            myServerSocket = new ServerSocket(8080);
////        }
////        catch(IOException ioe)
////        {
////            System.out.println("Could not create server socket on port 11111. Quitting.");
////            System.exit(-1);
////        }
////        Calendar now = Calendar.getInstance();
////        SimpleDateFormat formatter = new SimpleDateFormat("E yyyy.MM.dd 'at' hh:mm:ss a zzz");
////        System.out.println("It is now : " + formatter.format(now.getTime()));
////        while(ServerOn)
////        {
////            try
////            {
////                Socket clientSocket = myServerSocket.accept();
////                ClientServerThread cliThread = new ClientServerThread(clientSocket);
////                cliThread.start();
////
////            }
////            catch(IOException ioe)
////            {
////                System.out.println("Exception encountered on accept. Ignoring. Stack Trace :");
////                ioe.printStackTrace();
////            }
////
////        }
////
////        try
////        {
////            myServerSocket.close();
////            System.out.println("Server Stopped");
////        }
////        catch(Exception ioe)
////        {
////            System.out.println("Problem stopping server socket");
////            System.exit(-1);
////        }
////
////
////
////    }
////
////  //  public static void main (String[] args)
////  //  {
////        //new ChatServer();
////  //  }
////
////
//////    class ClientServiceThretharad extends Thread
//////    {
//////        Socket myClientSocket;
//////        boolean m_bRunThread = true;
//////
//////        public ClientServiceThread()
//////        {
//////            super();
//////        }
//////
//////        ClientServiceThread(Socket s)
//////        {
//////            myClientSocket = s;
//////
//////        }
//////
//////        public void run()
//////        {
//////            // Obtain the input stream and the output stream for the socket
//////            // A good practice is to encapsulate them with a BufferedReader
//////            // and a PrintWriter as shown below.
//////            BufferedReader in = null;
//////            PrintWriter out = null;
//////
//////            // Print out details of this connection
//////            System.out.println("Accepted Client Address - " + myClientSocket.getInetAddress().getHostName());
//////
//////            try
//////            {
//////                in = new BufferedReader(new InputStreamReader(myClientSocket.getInputStream()));
//////                out = new PrintWriter(new OutputStreamWriter(myClientSocket.getOutputStream()));
//////
//////                // At this point, we can read for input and reply with appropriate output.
//////
//////                // Run in a loop until m_bRunThread is set to false
//////                while(m_bRunThread)
//////                {
//////                    // read incoming stream
//////                    String clientCommand = in.readLine();
//////                    System.out.println("Client Says :" + clientCommand);
//////
//////                    if(!ServerOn)
//////                    {
//////                        // Special command. Quit this thread
//////                        System.out.print("Server has already stopped");
//////                        out.println("Server has already stopped");
//////                        out.flush();
//////                        m_bRunThread = false;
//////
//////                    }
//////
//////                    if(clientCommand.equalsIgnoreCase("quit")) {
//////                        // Special command. Quit this thread
//////                        m_bRunThread = false;
//////                        System.out.print("Stopping client thread for client : ");
//////                    } else if(clientCommand.equalsIgnoreCase("end")) {
//////                        // Special command. Quit this thread and Stop the Server
//////                        m_bRunThread = false;
//////                        System.out.print("Stopping client thread for client : ");
//////                        ServerOn = false;
//////                    } else {
//////                        // Process it
//////                        out.println("Server Says : " + clientCommand);
//////                        out.flush();
//////                    }
//////                }
//////            }
//////            catch(Exception e)
//////            {
//////                e.printStackTrace();
//////            }
//////            finally
//////            {
//////                // Clean up
//////                try
//////                {
//////                    in.close();
//////                    out.close();
//////                    myClientSocket.close();
//////                    System.out.println("...Stopped");
//////                }
//////                catch(IOException ioe)
//////                {
//////                    ioe.printStackTrace();
//////                }
//////            }
//////        }
//////
//////
//////    }
////}
///*
// * To change this license header, choose License Headers in Project Properties.
// * To change this template file, choose Tools | Templates
// * and open the template in the editor.
// */
//package com.example.tharuni.synomiliachat.Connection;
//
///**
// *
// * @author tharuni
// */
////import java.awt.*;
////import javax.swing.*;
//import java.net.*;
//import java.io.*;
//public class ChatServer implements Runnable
//{
//    ServerSocket ss;
//    Socket s1,s2;
//    BufferedReader br,br1;
//    PrintWriter pw,pw1;
//    Thread t1,t2;
//    String str;
//    public ChatServer()
//    {
//        try {
//            ss=new ServerSocket(8080);
//            s1=ss.accept();
//            s2=ss.accept();
//            br=new BufferedReader(new InputStreamReader(s1.getInputStream()));
//            br1=new BufferedReader(new InputStreamReader(s2.getInputStream()));
//            pw=new PrintWriter(s1.getOutputStream(),true);
//            pw1=new PrintWriter(s2.getOutputStream(),true);
//            t1=new Thread(this);
//            t2=new Thread(this);
//            t1.start();
//            t2.start();
//        }
//        catch(Exception ee)
//        {
//            System.out.println(ee);
//        }
//
//    }
//    public void run()
//    {
//        try {
//            while(true)
//            {
//                if(Thread.currentThread()==t1)
//                {
//                    str=br.readLine();
//                    pw1.println(str);
//                }
//                else
//                {
//                    str=br1.readLine();
//                    pw.println(str);
//                    Thread.sleep(600);
//                }
//            }
//        }
//        catch(Exception ee)
//        {
//            System.out.println(ee);
//        }
//    }
//    public static void main(String arg[])
//    {
//        new ChatServer();
//    }
//}
//

package com.example.tharuni.synomiliachat.Connection;

import java.net.ServerSocket;

/**
 * Created by tharuni on 28/03/2017.
 */

import java.net.*;
import java.io.*;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;

public class ChatServer {


/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author tharuni
 */


    /**
     * A multithreaded chat room server.  When a client connects the
     * server requests a screen name by sending the client the
     * text "SUBMITNAME", and keeps requesting a name until
     * a unique one is received.  After a client submits a unique
     * name, the server acknowledges with "NAMEACCEPTED".  Then
     * all messages from that client will be broadcast to all other
     * clients that have submitted a unique screen name.  The
     * broadcast messages are prefixed with "MESSAGE ".
     *
     */

    /**
     * The port that the server listens on.
     */
    private static final int PORT = 8080;

    /**
     * The set of all names of clients in the chat room.  Maintained
     * so that we can check that new clients are not registering name
     * already in use.
     */
    private static ArrayList<String> names = new ArrayList<String>();

    /**
     * The set of all the print writers for all the clients.  This
     * set is kept so we can easily broadcast messages.
     */
    private static ArrayList<PrintWriter> writers = new ArrayList<PrintWriter>();

    /**
     * The appplication main method, which just listens on a port and
     * spawns handler threads.
     */
    public static void main(String[] args) throws Exception {
        System.out.println("The chat server is running.");
        ServerSocket listener = new ServerSocket(PORT);
        try {
            while (true) {
                new Handler(listener.accept()).start();
            }
        } finally {
            listener.close();
        }
    }

    /**
     * A handler thread class.  Handlers are spawned from the listening
     * loop and are responsible for a dealing with a single client
     * and broadcasting its messages.
     */
    private static class Handler extends Thread {
        private String name;
        private Socket socket;
        private BufferedReader in;
        private PrintWriter out;

        /**
         * Constructs a handler thread, squirreling away the socket.
         * All the interesting work is done in the run method.
         */
        public Handler(Socket socket) {
            this.socket = socket;
        }

        /**
         * Services this thread's client by repeatedly requesting a
         * screen name until a unique one has been submitted, then
         * acknowledges the name and registers the output stream for
         * the client in a global set, then repeatedly gets inputs and
         * broadcasts them.
         */
        public void run() {
            try {

                // Create character streams for the socket.
                in = new BufferedReader(new InputStreamReader(
                        socket.getInputStream()));
                out = new PrintWriter(socket.getOutputStream(), true);

                // Request a name from this client.  Keep requesting until
                // a name is submitted that is not already used.  Note that
                // checking for the existence of a name and adding the name
                // must be done while locking the set of names.
                while (true) {
                    out.println("SUBMITNAME");
                    name = in.readLine();
                    if (name == null) {
                        return;
                    }
                    synchronized (names) {
                        if (!names.contains(name)) {
                            names.add(name);
                            break;
                        }
                    }
                }

                // Now that a successful name has been chosen, add the
                // socket's print writer to the set of all writers so
                // this client can receive broadcast messages.
                out.println("NAMEACCEPTED");
                writers.add(out);

                // Accept messages from this client and broadcast them.
                // Ignore other clients that cannot be broadcasted to.
                while (true) {
                    String input = in.readLine();
                    if (input == null) {
                        return;
                    }
                    for (PrintWriter writer : writers) {
                        writer.println("MESSAGE " + name + ": " + input);
                    }
                }
            } catch (IOException e) {
                System.out.println(e);


            } finally {
                // This client is going down!  Remove its name and its print
                // writer from the sets, and close its socket.
                if (name != null) {
                    names.remove(name);
                }
                if (out != null) {
                    writers.remove(out);
                }
                try {
                    socket.close();
                } catch (IOException e) {
                }
            }
        }
    }

}
