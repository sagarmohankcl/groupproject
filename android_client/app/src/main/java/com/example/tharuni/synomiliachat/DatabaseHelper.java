package com.example.tharuni.synomiliachat;

import android.database.sqlite.SQLiteOpenHelper;
import android.database.sqlite.SQLiteDatabase;
import android.content.Context;
import android.database.Cursor;

import java.util.ArrayList;
import java.util.List;
//import android.database.sqlite.SQLiteOpenHelper;
/**
 * Created by Sagar on 22/03/2017.
 */

public class DatabaseHelper extends SQLiteOpenHelper {
    public static final String DBNAME = "chatserver.sqlite";
    private static final String DATABASE_TABLE = "users";
    public static final String DBLOCATION = "/data/data/com.example.tharuni.synomiliachat/databases/";
    private Context mContext;
    private SQLiteDatabase mDatabase;

    public static final String Usernames = "username";

    public DatabaseHelper(Context context){
        super(context, DBNAME, null, 1);
        this.mContext = context;
    }

    @Override
    public void onCreate(SQLiteDatabase db){

    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion){

    }


    public void openDatabase(){
        String dbPath = mContext.getDatabasePath(DBNAME).getPath();
        if (mDatabase != null && mDatabase.isOpen()){
            return;
        }
        mDatabase = SQLiteDatabase.openDatabase(dbPath,null,SQLiteDatabase.OPEN_READWRITE);
    }

    public void closeDatabase(){
        if(mDatabase!=null){
            mDatabase.close();
        }
    }

    public List<Credentials> getListCredentials(){
        Credentials credentials = null;
        List<Credentials> credentialsList = new ArrayList<>();
        openDatabase();
        Cursor cursor = mDatabase.rawQuery("SELECT ROWID, * FROM USERS", null);
        cursor.moveToFirst();
        while(!cursor.isAfterLast()){
            credentials = new Credentials(cursor.getInt(0), cursor.getString(1), cursor.getString(2), cursor.getString(3), cursor.getString(4));
            credentialsList.add(credentials);
            cursor.moveToNext();
        }
        cursor.close();
        closeDatabase();
        return credentialsList;
    }

    public Cursor getAllRows(){
        String[] columns = {/*TABLE COLUMNS*/};
        return mDatabase.query(DATABASE_TABLE, columns, null, null, null, null, null);
    }


}
