import serial
import time

# Set up the serial connection
serial_port = '/dev/ttyUSB0'  # Replace with your actual port, e.g., COM3 for Windows
baud_rate = 9600  # Make sure this matches your Arduino's baud rate
ser = serial.Serial(serial_port, baud_rate, timeout=1)

def send_and_receive(command):
    """
    Sends a command to the Arduino, waits for a response, and returns three variables.
    
    Parameters:
        command (str): The command to send to Arduino.

    Returns:
        tuple: A tuple containing three variables if successful, or None if no response or invalid data.
    """
    # Send input to Arduino
    ser.write((command + "\n").encode('utf-8'))
    print(f"Sent: {command}")
    
    # Loop to wait for data with a timeout
    start_time = time.time()
    timeout = 5  # Set a timeout in seconds
    response = ""

    while (time.time() - start_time) < timeout:
        if ser.in_waiting > 0:
            response = ser.readline().decode('utf-8').strip()  # Read and decode response
            break
        time.sleep(0.1)  # Small delay to avoid busy waiting

    # Check if data was received within the timeout
    if response:
        print(f"Received: {response}")
        
        # Split the response by commas and assign to variables
        data_array = response.split(',')
        if len(data_array) >= 3:
            variable1 = data_array[0]
            variable2 = data_array[1]
            variable3 = data_array[2]
            
            # Return the variables as a tuple
            return variable1, variable2, variable3
        else:
            print("Invalid response format. Expected at least 3 items separated by commas.")
            return None
    else:
        print("No response received from Arduino within the timeout period.")
        return None

# Example of calling the function
try:
    result = send_and_receive("your_command_here")  # Replace with your actual command
    if result:
        variable1, variable2, variable3 = result
        print(f"Variable 1: {variable1}")
        print(f"Variable 2: {variable2}")
        print(f"Variable 3: {variable3}")
    else:
        print("Failed to retrieve data.")
except KeyboardInterrupt:
    print("\nProgram interrupted by user.")
finally:
    ser.close()
    print("Serial connection closed.")
