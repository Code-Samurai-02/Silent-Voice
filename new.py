import keyboard
import time

def my_task():
    print("Task Executed!")

while True:
    # Check if key 'a' is pressed (non-blocking)
    if keyboard.is_pressed('a'):
        my_task()
        time.sleep(0.3)   # debounce to avoid multiple triggers

    print("Loop running...")
    time.sleep(0.1)