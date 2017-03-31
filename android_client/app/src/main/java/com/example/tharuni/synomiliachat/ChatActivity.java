package com.example.tharuni.synomiliachat;

import android.os.AsyncTask;
import android.os.Build;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.content.Intent;
import com.example.tharuni.synomiliachat.ChatFunctionality.ChatAdapter;
import com.example.tharuni.synomiliachat.ChatFunctionality.ChatMessage;
import org.json.JSONObject;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.text.DateFormat;
import java.util.ArrayList;
import java.util.Date;
import static com.example.tharuni.synomiliachat.LoginActivity.globalUser;

public class ChatActivity extends AppCompatActivity {

    private EditText editText;
    private EditText searchText;
    private Button searchButton;
    private ListView listView;
    private Button sendBtn;
    private ChatAdapter adapter;
    private ArrayList<ChatMessage> chatHistory;
    private Socket client;
    private PrintWriter printWriter;
    private BufferedReader bufferedReader;
    private ChatMessage chatMessage;
    private JSONObject jsonObj;
    public static String CHAT_SERVER_IP = "10.40.207.97";


    /**
     * On Create method
     *
     * @param savedInstanceState
     */
    @Override
    protected void onCreate(Bundle savedInstanceState) {
       // Handler h = new Handler(ClientServerThread());

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_chat);
        editText = (EditText) findViewById(R.id.messageEdit);
        //  searchText = (EditText) findViewById(R.id.searchEdit);
        //  searchButton = (Button) findViewById(R.id.searchBtn);
        sendBtn = (Button) findViewById(R.id.chatSendButton);
        listView = (ListView) findViewById(R.id.messagesContainer);
        Button backBtn = (Button) findViewById(R.id.backBtn);
        initControls();

        backBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(ChatActivity.this, UserListActivity.class);
                startActivity(intent);
            }
        });
    }

    /**
     * @param menu
     * @return
     */
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    /**
     * @param item
     * @return
     */
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }


    public void initControls() {
        loadMessages();
        ChatOperator chatOperator = new ChatOperator();
        chatOperator.execute();
    }

    /**
     * Load Messages Method to load messages
     */
    private void loadMessages() {


        chatHistory = new ArrayList<ChatMessage>();
        ChatMessage msg = new ChatMessage();
        msg.setId(1);
        msg.setMe(false);
        String s = "WELCOME TO THE CHAT: "+globalUser;
        try {
            jsonObj = new JSONObject();
            jsonObj.put("MESSAGE", s);
        } catch (Exception e) {
        }
        msg.setMessage(jsonObj);
        msg.setDate(DateFormat.getDateTimeInstance().format(new Date()));
        chatHistory.add(msg);
        adapter = new ChatAdapter(ChatActivity.this, new ArrayList<ChatMessage>());
        listView.setAdapter(adapter);
        for (int i = 0; i < chatHistory.size(); i++) {
            ChatMessage message = chatHistory.get(i);
            displayMessage(message);

        }

    }

    /**
     * @param message
     */
    public void displayMessage(ChatMessage message) {
        adapter.add(message);
        adapter.notifyDataSetChanged();
        scroll();
    }

    /**
     *
     */
    private void scroll() {

        listView.setSelection(listView.getCount() - 1);
    }


    /**
     * This AsyncTask create the connection with the server and initialize the
     * chat senders and receivers.
     */
    private class ChatOperator extends AsyncTask<Void, Void, Void> {

        @Override
        protected Void doInBackground(Void... arg0) {
            try {
                client = new Socket("10.40.216.156", 8080); // Creating the server socket.

                if (client != null) {
                    printWriter = new PrintWriter(client.getOutputStream(), true);
                    InputStreamReader inputStreamReader = new InputStreamReader(client.getInputStream());
                    bufferedReader = new BufferedReader(inputStreamReader);
                } else {
                    System.out.println("Server has not bean started on port ::::");
                }
            } catch (UnknownHostException e) {
                System.out.println("Faild to connect server " + CHAT_SERVER_IP);
                e.printStackTrace();
            } catch (IOException e) {
                System.out.println("Faild to connect server " + CHAT_SERVER_IP);
                e.printStackTrace();
            }
            return null;
        }

        /**
         * Following method is executed at the end of doInBackground method.
         */
        @Override
        protected void onPostExecute(Void result) {
            sendBtn.setOnClickListener(new View.OnClickListener() {
                public void onClick(View v) {
                    final Sender messageSender = new Sender(); // Initialize chat sender AsyncTask.
                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.HONEYCOMB) {
                        messageSender.executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR);
                    } else {
                        messageSender.execute();
                    }
                }
            });
//
//            searchButton.setOnClickListener((new View.OnClickListener() {
//                @Override
//                public void onClick(View v)
//                {
//                    final Sender messageSender = new Sender(); // Initialize chat sender AsyncTask.
//                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.HONEYCOMB) {
//                        messageSender.executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR);
//                    } else {
//                       // Socket socket = new Socket();
//                        messageSender.execute();
//                        try {
//                            Socket s = new Socket(getConnection, 8080);
//                        }catch (Exception e){}
//                    }
//                }
//            }));
            Receiver receiver = new Receiver(); // Initialize chat receiver AsyncTask.
            receiver.execute();
        }
    }

    /**
     * This AsyncTask continuously reads the input buffer and show the chat
     * message if a message is availble.
     */
    private class Receiver extends AsyncTask<Void, Void, Void> {
        private String message;

        @Override
        protected Void doInBackground(Void... params) {
            while (true) {
                try {

                    if (bufferedReader.ready()) {
                        message = bufferedReader.readLine();
                        publishProgress(null);
                    }
                } catch (UnknownHostException e) {
                    e.printStackTrace();
                } catch (IOException e) {
                    e.printStackTrace();
                }

                try {
                    Thread.sleep(500);
                } catch (InterruptedException ie) {
                }
            }
        }

        @Override
        protected void onProgressUpdate(Void... values) {
            JSONObject obj = new JSONObject();
            try {
                obj.put("MSG", message);
            } catch (Exception e) {
            }
            ChatMessage chatMessage = new ChatMessage();
            chatMessage.setMe(false);
            chatMessage.setMessage(obj);
            chatMessage.setDate(DateFormat.getDateTimeInstance().format(new Date()));
            displayMessage(chatMessage);
        }

    }

    /**
     * This AsyncTask sends the chat message through the output stream.
     */
    private class Sender extends AsyncTask<Void, Void, Void> {
        JSONObject obj = new JSONObject();
        private String message;

        @Override
        protected Void doInBackground(Void... params) {
            message = editText.getText().toString();
            EditText et = (EditText) findViewById(R.id.username);
            try {
//                jsonObj.put("OPTION","SEARCH USER");
//                jsonObj.put("USER",searchText.getText().toString());
                obj.put("USER", globalUser);
                obj.put("Message: ", message);
                // obj.toString();
            } catch (Exception e) {
            }
            printWriter.write(obj.toString() + "\n");
            printWriter.flush();
            return null;
        }

        @Override
        protected void onPostExecute(Void result) {
            ChatMessage chatMessage = new ChatMessage();
            chatMessage.setMe(true);
            editText.setText(""); // Clear the chat box
            chatMessage.setMessage(obj);
            chatMessage.setDate(DateFormat.getDateTimeInstance().format(new Date()));
            displayMessage(chatMessage);

//            try {
//                getConnection = jsonObj.getJSONArray("CONNECTION").toString();
//            }catch (Exception e){}
        }
    }


}



