# Silent Voice Android App

This is a native Android application that replicates the functionality of the Python `receiver.py`. It connects to a paired Bluetooth SPP module (like HC-05), reads incoming character streams, parses valid words (using `*` for append and `.` for finish), and natively reads them out using Android's Text-to-Speech (TTS) engine.

## Prerequisites
- Android Studio installed on your computer.
- An Android Phone (API Level 21 / Android 5.0 or higher).
- A hardware glove setup with a Bluetooth SPP Module (e.g., HC-05/ESP32).

## How to Build and Run after `git clone`

1. **Clone the Repository**
   If you (or someone else) cloned the repository, the complete Android project is located inside the `app/` directory.

2. **Open in Android Studio**
   - Open Android Studio.
   - On the welcome screen, click **Open** (or go to `File` -> `Open`).
   - Navigate to the cloned repository and exactly select the `app` folder (e.g., `Silent-Voice/app`).
   - Click **OK**.
   - **Important:** Do *not* open the root `Silent-Voice` folder in Android Studio, as it won't recognize the Gradle configuration properly. Only open the `app` directory.

3. **Wait for Gradle Sync**
   - Android Studio will start downloading necessary Gradle wrapper files and Android SDK dependencies.
   - Wait until the build sync finishes successfully (indicated by a green checkmark at the bottom).

4. **Connect your Android Device**
   - Enable **Developer Options** and **USB Debugging** on your Android phone.
   - Connect the phone to your computer via USB.
   - If prompted on the phone, allow USB debugging.
   - Your device should now appear in the dropdown menu at the top center of Android Studio next to the "Run" (Play) button.

5. **Run the Application**
   - Click the green **Run 'app'** (Play icon) button or press `Shift + F10`.
   - Android Studio will compile the code and install the application directly onto your connected phone.

## How to Use the App with Hardware

1. Turn on your glove/hardware so the Bluetooth module is broadcasting.
2. Go into your Android Phone’s Bluetooth Settings. Ensure it is paired with the hardware module (e.g., HC-05).
3. Open the installed **Silent Voice** app on your phone.
4. Select the language (English or Hindi) using the radio buttons.
> **Note:** For Hindi playback, ensure your phone has Hindi Voice Data installed in its Text-to-Speech settings.
5. Tap **Connect paired Bluetooth Device**.
6. A popup list of your paired Bluetooth devices will appear. Select your glove module (HC-05).
7. The logs will say "Connected" and the button will turn gray.
8. Perform the gestures. As characters are sent via serial, they will appear on the screen.
9. When the `.` command is sent, the app will clear the text and speak the entire accumulated word out loud.
