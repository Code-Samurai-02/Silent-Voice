package com.silentvoice.app;

import android.Manifest;
import android.annotation.SuppressLint;
import android.app.AlertDialog;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Bundle;
import android.widget.Button;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;

public class MainActivity extends AppCompatActivity implements MessageParser.MessageListener {

    private static final int PERMISSION_REQUEST_BLUETOOTH = 1;
    
    // UI Elements
    private RadioGroup rgLanguage;
    private RadioButton rbEnglish, rbHindi;
    private Button btnConnect;
    private TextView tvMessage, tvLogs;

    // Services
    private TTSManager ttsManager;
    private BluetoothSPPService btService;
    private MessageParser messageParser;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Bind UI
        rgLanguage = findViewById(R.id.rgLanguage);
        rbEnglish = findViewById(R.id.rbEnglish);
        rbHindi = findViewById(R.id.rbHindi);
        btnConnect = findViewById(R.id.btnConnect);
        tvMessage = findViewById(R.id.tvMessage);
        tvLogs = findViewById(R.id.tvLogs);

        // Init Managers
        ttsManager = new TTSManager(this);
        messageParser = new MessageParser(this);
        
        btService = new BluetoothSPPService(new BluetoothSPPService.BluetoothListener() {
            @Override
            public void onDataReceived(String data) {
                messageParser.parse(data);
            }

            @Override
            public void onError(String error) {
                logMessage("Error: " + error);
                btnConnect.setEnabled(true);
                btnConnect.setText("Connect paired Bluetooth Device");
            }

            @Override
            public void onConnected() {
                logMessage("Connected to device successfully");
                btnConnect.setText("Connected");
            }
        });

        rgLanguage.setOnCheckedChangeListener((group, checkedId) -> {
            if (checkedId == R.id.rbEnglish) {
                ttsManager.setLanguageEnglish();
                logMessage("Language changed to English");
            } else if (checkedId == R.id.rbHindi) {
                ttsManager.setLanguageHindi();
                logMessage("Language changed to Hindi");
            }
        });

        btnConnect.setOnClickListener(v -> checkBluetoothPermissionsAndConnect());
    }

    private void checkBluetoothPermissionsAndConnect() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            if (ActivityCompat.checkSelfPermission(this, Manifest.permission.BLUETOOTH_CONNECT) != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(this, new String[]{
                        Manifest.permission.BLUETOOTH_CONNECT,
                        Manifest.permission.BLUETOOTH_SCAN
                }, PERMISSION_REQUEST_BLUETOOTH);
                return;
            }
        }
        showDeviceList();
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == PERMISSION_REQUEST_BLUETOOTH) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                showDeviceList();
            } else {
                Toast.makeText(this, "Bluetooth permission required", Toast.LENGTH_SHORT).show();
            }
        }
    }

    @SuppressLint("MissingPermission")
    private void showDeviceList() {
        BluetoothAdapter btAdapter = BluetoothAdapter.getDefaultAdapter();
        if (btAdapter == null || !btAdapter.isEnabled()) {
            Toast.makeText(this, "Please enable Bluetooth", Toast.LENGTH_SHORT).show();
            return;
        }

        Set<BluetoothDevice> pairedDevices = btAdapter.getBondedDevices();
        if (pairedDevices.isEmpty()) {
            Toast.makeText(this, "No paired devices found", Toast.LENGTH_SHORT).show();
            return;
        }

        List<BluetoothDevice> deviceList = new ArrayList<>(pairedDevices);
        String[] deviceNames = new String[deviceList.size()];
        for (int i = 0; i < deviceList.size(); i++) {
            deviceNames[i] = deviceList.get(i).getName() + "\n" + deviceList.get(i).getAddress();
        }

        new AlertDialog.Builder(this)
                .setTitle("Select Paired Device")
                .setItems(deviceNames, (dialog, which) -> {
                    BluetoothDevice device = deviceList.get(which);
                    logMessage("Connecting to " + device.getName() + "...");
                    btnConnect.setEnabled(false);
                    btnConnect.setText("Connecting...");
                    btService.connect(device);
                })
                .show();
    }

    private void logMessage(String msg) {
        runOnUiThread(() -> {
            String currentLogs = tvLogs.getText().toString();
            tvLogs.setText(msg + "\n" + currentLogs);
        });
    }

    // MessageListener Implementation
    @Override
    public void onCharacterAppended(char c, String currentTemp) {
        runOnUiThread(() -> tvMessage.setText(currentTemp + "_"));
    }

    @Override
    public void onMessageComplete(String fullMessage) {
        runOnUiThread(() -> {
            tvMessage.setText(fullMessage);
            logMessage("Spoke: " + fullMessage);
            ttsManager.speak(fullMessage);
        });
    }

    @Override
    public void onLog(String logMessage) {
        logMessage(logMessage);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        btService.stop();
        ttsManager.shutdown();
    }
}
