package com.example.tharuni.synomiliachat;

/**
 * Created by Sagar on 22/03/2017.
 */

public class Credentials {

    private int rowId;
    private String username;
    private String password;
    private String connection;
    private String date;

    public Credentials(int rowId, String username, String password, String connection, String date) {
        this.rowId = rowId;
        this.username = username;
        this.password = password;
        this.connection = connection;
        this.date = date;
    }


    public int getrowId() {
        return rowId;
    }
//
    public String getUsername() {
        return username;
    }
//
    public void setId(int rowId) {
        this.rowId = rowId;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getConnection() {
        return connection;
    }

    public void setConnection(String connection) {
        this.connection = connection;
    }

    public String getDate() {
        return date;
    }

    public void setDate(String date) {
        this.date = date;
    }
}
