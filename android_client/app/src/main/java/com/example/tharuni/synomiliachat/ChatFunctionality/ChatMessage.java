package com.example.tharuni.synomiliachat.ChatFunctionality;

/**
 * Created by tharuni on 08/03/2017.
 */

import org.json.JSONObject;

/**
     * Created by Technovibe on 17-04-2015.
     */
    public class ChatMessage {
        private long id;
        private boolean isMe;
        private JSONObject message;
        private Long userId;
        private String dateTime;


//    public ChatMessage(long id,boolean isMe,JSONObject message,Long userId,String dateTime)
//    {
//        this.id=id;
//        this.isMe=isMe;
//        this.message=message;
//        this.userId=userId;
//        this.dateTime=dateTime;
//    }

        public long getId() {
            return id;
        }

        public void setId(long id) {
            this.id = id;
        }

        public boolean getIsme() {
            return isMe;
        }

        public void setMe(boolean isMe) {
            this.isMe = isMe;
        }

        public JSONObject getMessage() {
            return message;
        }

        public void setMessage(JSONObject message) {
            this.message = message;
        }

        public long getUserId() {
            return userId;
        }

        public void setUserId(long userId) {
            this.userId = userId;
        }

        public String getDate() {
            return dateTime;
        }

        public void setDate(String dateTime) {
            this.dateTime = dateTime;
        }
    }




