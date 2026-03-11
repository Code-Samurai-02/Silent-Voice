package com.silentvoice.app;

import android.os.SystemClock;
import android.util.Log;

import java.util.HashSet;
import java.util.Set;

public class MessageParser {
    private static final String TAG = "MessageParser";
    private static final long STAR_DEBOUNCE_MS = 500;
    
    private final Set<Character> validLetters;
    private String temp = "";
    private Character lastLetter = null;
    private long lastStarTime = 0;

    public interface MessageListener {
        void onCharacterAppended(char c, String currentTemp);
        void onMessageComplete(String fullMessage);
        void onLog(String logMessage);
    }

    private MessageListener listener;

    public MessageParser(MessageListener listener) {
        this.listener = listener;
        validLetters = new HashSet<>();
        for (char c = 'A'; c <= 'Z'; c++) {
            validLetters.add(c);
        }
    }

    public void parse(String data) {
        if (data == null || data.isEmpty() || data.equals("Error")) {
            return;
        }

        // Handle string if more than 1 length? In Python it looks like length 1 chars are sent.
        // Or "Error" which is handled.
        // Assuming data is single character string usually (except Error).
        if (data.length() > 1 && !data.equals("Error")) {
            // But receiver.py does data = ser.readline() which may include full line.
            // receiver.py expects single characters like 'A', '*', ' ', '.'
            data = data.trim();
            if (data.isEmpty()) return;
        }
        
        // Take the first character if it's sent as a string like "A "
        char c = data.charAt(0);

        if (validLetters.contains(c)) {
            lastLetter = c;
            log("Stored: " + lastLetter);
        } else if (c == ' ') {
            temp += " ";
            log("Added space");
        } else if (c == '*') {
            long currentTime = SystemClock.elapsedRealtime();

            if ((currentTime - lastStarTime) < STAR_DEBOUNCE_MS) {
                return; // ignore repeated star
            }

            lastStarTime = currentTime;

            if (lastLetter != null) {
                temp += lastLetter;
                log("Appended: " + lastLetter);
                if (listener != null) {
                    listener.onCharacterAppended(lastLetter, temp);
                }
                lastLetter = null;
            }
        } else if (c == '.') {
            log("Final Output: " + temp);
            if (listener != null) {
                listener.onMessageComplete(temp);
            }
            temp = "";
            lastLetter = null;
        }
    }

    private void log(String message) {
        Log.d(TAG, message);
        if (listener != null) {
            listener.onLog(message);
        }
    }
}
