# 2025 EAIT HACKATHON; WALL-E Waste System

This current prototype basically identifies a type of trash, then moves the servo either right or left. The idea is similar to plinko, except which direction it goes is not randomised, but rather dependent on the type of trash it is.

# How to run the code
pip install -r requirements.txt

Flash StandardFirmata Code to Arduino Nano
In main.py, change the upload port to one you use (you can see this in arduinoIDE in the bottom right)
Wire the servo motor to pin d9

run main.py