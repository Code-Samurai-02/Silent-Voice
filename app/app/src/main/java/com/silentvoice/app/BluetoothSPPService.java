package com.silentvoice.app;

import android.annotation.SuppressLint;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.os.Handler;
import android.os.Looper;
import android.util.Log;

import java.io.IOException;
import java.io.InputStream;
import java.util.UUID;

public class BluetoothSPPService {
    private static final String TAG = "BluetoothSPP";
    // Standard SPP UUID
    private static final UUID SPP_UUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB");

    private BluetoothAdapter bluetoothAdapter;
    private BluetoothSocket socket;
    private ConnectedThread connectedThread;
    private final Handler mainHandler;
    
    public interface BluetoothListener {
        void onDataReceived(String data);
        void onError(String error);
        void onConnected();
    }

    private BluetoothListener listener;

    public BluetoothSPPService(BluetoothListener listener) {
        this.listener = listener;
        this.bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
        this.mainHandler = new Handler(Looper.getMainLooper());
    }

    @SuppressLint("MissingPermission")
    public void connect(BluetoothDevice device) {
        new Thread(() -> {
            try {
                socket = device.createRfcommSocketToServiceRecord(SPP_UUID);
                bluetoothAdapter.cancelDiscovery();
                socket.connect();
                
                mainHandler.post(() -> {
                    if (listener != null) listener.onConnected();
                });

                connectedThread = new ConnectedThread(socket);
                connectedThread.start();
            } catch (IOException e) {
                Log.e(TAG, "Connect error", e);
                mainHandler.post(() -> {
                    if (listener != null) listener.onError("Connection failed: " + e.getMessage());
                });
                try {
                    if (socket != null) socket.close();
                } catch (IOException ignored) {}
            }
        }).start();
    }

    public void stop() {
        if (connectedThread != null) {
            connectedThread.cancel();
            connectedThread = null;
        }
    }

    private class ConnectedThread extends Thread {
        private final BluetoothSocket mmSocket;
        private final InputStream mmInStream;

        public ConnectedThread(BluetoothSocket socket) {
            mmSocket = socket;
            InputStream tmpIn = null;
            try {
                tmpIn = socket.getInputStream();
            } catch (IOException e) {
                Log.e(TAG, "Error occurred when creating input stream", e);
            }
            mmInStream = tmpIn;
        }

        public void run() {
            byte[] mmBuffer = new byte[1024];
            int numBytes; 

            // Read line by line logic similar to readline
            StringBuilder readMessage = new StringBuilder();

            while (true) {
                try {
                    numBytes = mmInStream.read(mmBuffer);
                    String tempVal = new String(mmBuffer, 0, numBytes);
                    readMessage.append(tempVal);
                    
                    int endOfLineIndex = readMessage.indexOf("\n");
                    while (endOfLineIndex > 0) {
                        String dataLine = readMessage.substring(0, endOfLineIndex);
                        readMessage.delete(0, endOfLineIndex + 1);
                        
                        dataLine = dataLine.replace("\r", "").replace("\n", "");
                        if (!dataLine.isEmpty()) {
                            final String finalData = dataLine;
                            mainHandler.post(() -> {
                                if (listener != null) listener.onDataReceived(finalData);
                            });
                        }
                        endOfLineIndex = readMessage.indexOf("\n");
                    }
                } catch (IOException e) {
                    Log.d(TAG, "Input stream was disconnected", e);
                    mainHandler.post(() -> {
                        if (listener != null) listener.onError("Connection lost");
                    });
                    break;
                }
            }
        }

        public void cancel() {
            try {
                mmSocket.close();
            } catch (IOException e) {
                Log.e(TAG, "Could not close the connect socket", e);
            }
        }
    }
}
