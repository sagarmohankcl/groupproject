package com.example.tharuni.synomiliachat.RecyclerViewAdapter;

import android.content.Intent;
import android.support.v7.widget.RecyclerView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import android.content.Context;

import com.example.tharuni.synomiliachat.ChatActivity;
import com.example.tharuni.synomiliachat.FragContent.ChatFragContent;
import com.example.tharuni.synomiliachat.Fragments.ChatFragment;
import com.example.tharuni.synomiliachat.Fragments.ChatFragment.OnListFragmentInteractionListener;
import com.example.tharuni.synomiliachat.FragContent.ChatFragContent.Chat;
import com.example.tharuni.synomiliachat.MainActivity;
import com.example.tharuni.synomiliachat.R;

import java.util.List;

/**
 * {@link RecyclerView.Adapter} that can display a {@link Chat} and makes a call to the
 * specified {@link OnListFragmentInteractionListener}.
 * TODO: Replace the implementation with code for your data type.
 */
public class MyChatRecyclerViewAdapter extends RecyclerView.Adapter<MyChatRecyclerViewAdapter.ViewHolder> {

    public interface ItemClickListener{
        void onClick(View view, int position, boolean isLongClick);
    }

    private final List<Chat> mValues;
    private final OnListFragmentInteractionListener mListener;
    private Context context;

    public MyChatRecyclerViewAdapter(List<Chat> items, OnListFragmentInteractionListener listener) {
        mValues = items;
        //this.context = contexts;
        mListener = listener;
    }

    @Override
    public ViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.fragment_chat, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(final ViewHolder holder, int position) {
        holder.mItem = mValues.get(position);
        holder.mIdView.setText(mValues.get(position).id);
        holder.mContentView.setText(mValues.get(position).content);
        holder.setClickListener(new ItemClickListener() {
            @Override
            public void onClick(View view, int position, boolean isLongClick) {
                if (isLongClick) {
                    Intent intent = new Intent(context, ChatActivity.class);
                    context.startActivity(intent);
                } else {

                    Intent intent = new Intent(context, ChatActivity.class);
                    context.startActivity(intent);

                    //((MainActivity) getActivity()).startActivity(intent);
                }
            }
        });
        holder.mView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (null != mListener) {
                    // Notify the active callbacks interface (the activity, if the
                    // fragment is attached to one) that an item has been selected.
                    mListener.onListFragmentInteraction(holder.mItem);
                }
            }
        });
    }

    @Override
    public int getItemCount() {
        return mValues.size();
    }

    public class ViewHolder extends RecyclerView.ViewHolder implements View.OnClickListener, View.OnLongClickListener{
        public final View mView;
        public final TextView mIdView;
        public final TextView mContentView;
        private ItemClickListener clickListener;
        public Chat mItem;
        public ViewHolder(View view) {
            super(view);
            context = itemView.getContext();
            mView = view;
            mIdView = (TextView) view.findViewById(R.id.id);
            mContentView = (TextView) view.findViewById(R.id.content);
            view.setOnClickListener(this);
            view.setOnLongClickListener(this);

        }

        public void setClickListener(ItemClickListener itemClickListener) {
            this.clickListener = itemClickListener;
        }

        public void onClick(View view) {
            clickListener.onClick(view, getPosition(), false);
        }

        public boolean onLongClick(View view) {
            clickListener.onClick(view, getPosition(), true);
            return true;
        }

        @Override
        public String toString() {
            return super.toString() + " '" + mContentView.getText() + "'";
        }
    }
}
