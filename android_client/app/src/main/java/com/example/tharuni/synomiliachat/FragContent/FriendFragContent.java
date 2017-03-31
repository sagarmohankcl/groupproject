package com.example.tharuni.synomiliachat.FragContent;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Helper class for providing sample content for user interfaces created by
 * Android template wizards.
 * <p>
 * TODO: Replace all uses of this class before publishing your app.
 */
public class FriendFragContent {

    /**
     * An array of sample (dummy) items.
     */
    public static final List<Friend> ITEMS = new ArrayList<Friend>();

    /**
     * A map of sample (dummy) items, by ID.
     */
    public static final Map<String, Friend> ITEM_MAP = new HashMap<String, Friend>();

    private static final int COUNT = 25;

    static {
        // Add some sample items.
        for (int i = 1; i <= COUNT; i++) {
            addItem(createDummyItem(i));
        }
    }

    private static void addItem(Friend friend) {
        ITEMS.add(friend);
        ITEM_MAP.put(friend.id, friend);
    }

    private static Friend createDummyItem(int position) {
        return new Friend(String.valueOf(position), "Item " + position, makeDetails(position));
    }

    private static String makeDetails(int position) {
        StringBuilder builder = new StringBuilder();
        builder.append("Details about Item: ").append(position);
        for (int i = 0; i < position; i++) {
            builder.append("\nMore details information here.");
        }
        return builder.toString();
    }

    /**
     * A dummy item representing a piece of content.
     */
    public static class Friend {
        public final String id;
        public final String content;
        public final String details;

        public Friend(String id, String content, String details) {
            this.id = id;
            this.content = content;
            this.details = details;
        }

        @Override
        public String toString() {
            return content;
        }
    }
}
