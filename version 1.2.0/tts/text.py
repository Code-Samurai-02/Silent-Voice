from tts_client import connect, speak, disconnect


def main():
    connect()

    while True:
        text = input("You: ").strip()

        if text.lower() == "exit":
            break

        if text:
            speak(text)

    disconnect()


if __name__ == "__main__":
    main()