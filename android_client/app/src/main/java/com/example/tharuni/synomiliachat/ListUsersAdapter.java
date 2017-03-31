package com.example.tharuni.synomiliachat; /**
 * Created by Sagar on 22/03/2017.
 */

import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.content.Context;
import android.view.View;
import android.widget.ListAdapter;
import android.widget.TextView;
import android.widget.ListView;

import org.w3c.dom.Text;

import java.util.List;
import java.util.Map;


public class ListUsersAdapter extends BaseAdapter {

    private Context mContext;
    private long row;
    private List<Credentials> sUsersList;

    public ListUsersAdapter(Context mContext, List<Credentials> sUsersList) {
        this.mContext = mContext;
        this.sUsersList = sUsersList;
    }

    @Override
    public int getCount(){
        return sUsersList.size();
    }

    @Override
    public Object getItem(int position){
        return sUsersList.get(position);
    }


    @Override
    public long getItemId(int position) {
        return sUsersList.get(position).getrowId();
    }


    @Override
    public View getView(int position, View convertView, ViewGroup parent){
        View v = View.inflate(mContext, R.layout.user_listview, null);
        TextView tvName = (TextView) v.findViewById(R.id.tv_username);
//        TextView tvPassword = (TextView)v.findViewById(R.id.tv_password);
//        TextView tvConnection = (TextView)v.findViewById(R.id.tv_connection);
//        TextView tvDate = (TextView)v.findViewById(R.id.tv_date);

          tvName.setText(sUsersList.get(position).getUsername());
//        tvPassword.setText(sUsersList).get(position).getPassword();
//        tvConnection.setText(sUsersList).get(position).getConnection();
//        tvDate.setText(sUsersList).get(position).getDate();

        return v;
    }





}
