package com.silentvoice.app;

import android.content.Context;
import android.speech.tts.TextToSpeech;
import android.util.Log;

import java.util.Locale;

public class TTSManager implements TextToSpeech.OnInitListener {
    private TextToSpeech tts;
    private boolean isReady = false;
    private Locale currentLocale = Locale.US;

    public TTSManager(Context context) {
        tts = new TextToSpeech(context, this);
    }

    @Override
    public void onInit(int status) {
        if (status == TextToSpeech.SUCCESS) {
            isReady = true;
            setLanguage(currentLocale);
            Log.d("TTSManager", "TTS Initialized");
        } else {
            Log.e("TTSManager", "TTS Initialization failed");
        }
    }

    public void setLanguage(Locale locale) {
        this.currentLocale = locale;
        if (isReady) {
            int result = tts.setLanguage(locale);
            if (result == TextToSpeech.LANG_MISSING_DATA || result == TextToSpeech.LANG_NOT_SUPPORTED) {
                Log.e("TTSManager", "Language not supported: " + locale.toString());
            }
        }
    }

    public void setLanguageEnglish() {
        setLanguage(Locale.US);
    }

    public void setLanguageHindi() {
        setLanguage(new Locale("hi", "IN"));
    }

    public void speak(String text) {
        if (isReady && text != null && !text.isEmpty()) {
            tts.speak(text, TextToSpeech.QUEUE_FLUSH, null, null);
        }
    }

    public void shutdown() {
        if (tts != null) {
            tts.stop();
            tts.shutdown();
        }
    }
}
