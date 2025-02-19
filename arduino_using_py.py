import serial
import time

arduino_port = 'COM3' # COM9
baud_rate = 9600

try:
    # Initialize serial connection
    arduino = serial.Serial(arduino_port, baud_rate, timeout=1)
    time.sleep(2)  # Wait for Arduino to reset

    print("Connection to Arduino established.")

    while True:
        
        print("F: Move motor forward")
        print("R: Move motor in reverse")
        print("S: Stop the motor")
        print("Q: Quit the program")
        command = input("Enter your command: ").strip().upper()

        if command == 'Q':
            print("Exiting program.")
            break

        if command not in ['F', 'R', 'S']:
            print("Invalid command. Try again.")
            continue

        arduino.write(command.encode())  # Send command to Arduino
        time.sleep(0.1)  # Give Arduino time to process
        response = arduino.readline().decode('utf-8').strip()  # Read response
        print("Arduino response:", response)

except serial.SerialException as e:
    print(f"Error connecting to Arduino: {e}")

finally:
    if 'arduino' in locals() and arduino.is_open:
        arduino.close()
        print("Serial connection closed.")
