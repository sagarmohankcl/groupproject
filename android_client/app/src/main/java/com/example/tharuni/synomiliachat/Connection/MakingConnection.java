package com.example.tharuni.synomiliachat.Connection;

import android.os.AsyncTask;
import android.widget.TextView;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.Socket;
import java.net.UnknownHostException;

/**
 * Created by tharuni on 06/03/2017.
 */


    public class MakingConnection extends AsyncTask<Void, Void, Void> {

        String dstAddress = "localhost";
        int dstPort = 8080;
      //  String response = "";
        TextView textResponse;

        public MakingConnection(String addr, int port) {
            dstAddress = addr;
            dstPort = port;
           //this.textResponse=textResponse;
        }

        @Override
        protected Void doInBackground(Void... arg0) {

            Socket socket = null;

            try {
                socket = new Socket(dstAddress, dstPort);

                ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream(
                        1024);
                byte[] buffer = new byte[1024];

                int bytesRead;
                InputStream inputStream = socket.getInputStream();


			 // notice: inputStream.read() will block if no data return

               while ((bytesRead = inputStream.read(buffer)) != -1) {
                    byteArrayOutputStream.write(buffer, 0, bytesRead);
                //    response += byteArrayOutputStream.toString("UTF-8");
                }

            } catch (UnknownHostException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
               // response = "UnknownHostException: " + e.toString();
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
                //response = "IOException: " + e.toString();
            } finally {
                if (socket != null) {
                    try {
                        socket.close();
                    } catch (IOException e) {
                        // TODO Auto-generated catch block
                        e.printStackTrace();
                    }
                }
            }
            return null;
        }

        @Override
        protected void onPostExecute(Void result) {
           // textResponse.setText(response);
            super.onPostExecute(result);
        }

    }


