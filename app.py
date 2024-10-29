from flask import Flask, render_template, Response
import threading
import playsound
import printer
import serial
import time
import math
import db_module
from datetime import datetime

app = Flask(__name__)

#Variables files Location#
music_welcome = "static/audio/welcome.mp3"
music_next = "static/audio/next.mp3"
music_complete = "static/audio/complete.mp3"
music_heavy = "static/audio/heavy.mp3"
music_Hwelcome = "static/audio/Hwelcome.mp3"
music_Hnext = "static/audio/Hnext.mp3"
music_Hcomplete = "static/audio/Hcomplete.mp3"
music_Hheavy = "static/audio/Hheavy.mp3"
music_Iwelcome = "static/audio/Iwelcome.mp3"
music_Inext = "static/audio/Inext.mp3"
music_Icomplete = "static/audio/Icomplete.mp3"
music_Iheavy = "static/audio/Iheavy.mp3"
music_Ywelcome = "static/audio/Ywelcome.mp3"
music_Ynext = "static/audio/Ynext.mp3"
music_Ycomplete = "static/audio/Ycomplete.mp3"
music_Yheavy = "static/audio/Yheavy.mp3" 
#Audio Files Location Close#

#Sound Files#
def in_sound():
    playsound.play_music(music_welcome)
def in_Hsound():
	playsound.play_music(music_Hwelcome)
def in_Isound():
	playsound.play_music(music_Iwelcome)
def in_Ysound():
	playsound.play_music(music_Ywelcome)
def in_sounds():
	playsound.play_music(music_complete)
def in_Hsounds():
	playsound.play_music(music_Hcomplete)
def in_Isounds():
	playsound.play_music(music_Icomplete)
def in_Ysounds():
	playsound.play_music(music_Ycomplete)
def in_next():
    playsound.play_music(music_next)
#Functions for sound#

start_button = 0
complete_button = False
print_button = 0
Total_weight_value = 0
Total_point_value = 0
Total_canw_value = 0
Total_bottlew_value = 0
Total_can_value = 0
Total_plastic_value = 0

serial_port = '/dev/ttyUSB0'  # Replace with your actual port, e.g., COM3 for Windows
baud_rate = 9600  # Make sure this matches your Arduino's baud rate
ser = serial.Serial(serial_port, baud_rate, timeout=1)

def send_and_receive(command):
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
            variable1 = int(data_array[0])
            variable2 = int(data_array[1])
            variable3 = int(data_array[2])
            
            # Return the variables as a tuple
            return variable1, variable2, variable3
        else:
            print("Invalid response format. Expected at least 3 items separated by commas.")
            return None
    else:
        print("No response received from Arduino within the timeout period.")
        return None




def main():

    total_weight = 0
    total_point = 0
    tbottle_weight = 0
    tcan_weight = 0
    bottle_count = 0
    can_count = 0
    global Total_weight_value,Total_point_value,Total_canw_value,Total_bottlew_value,Total_can_value,Total_plastic_value,session_id

    db_module.create_table()
    session_id = db_module.create_session_id()
    created = datetime.now()

    while True:
        result = send_and_receive("readnew") 
        if result:
            weight, matType, errorFlag = result
                
            if errorFlag == 1 and matType == 2:
                total_weight += weight
                can_count += 1
                tcan_weight += weight
                playsound.play_music(music_next)

            if errorFlag == 1 and matType ==1:
               total_weight += weight
               bottle_count += 1
               tbottle_weight += weight
               playsound.play_music(music_next)

            if errorFlag == 0 and weight > 5:
               playsound.play_music(music_heavy)
            
        
        if complete_button:
            break
        
        Total_weight_value = total_weight
        Total_point_value = total_point
        Total_canw_value = tcan_weight
        Total_bottlew_value = tbottle_weight
        Total_can_value = can_count
        Total_plastic_value = bottle_count

        # Insert the current values into the database
        modified = datetime.now()
        db_module.insert_or_update_values(can_count, tcan_weight, bottle_count, tbottle_weight,created,modified,session_id)
        

def hmain():

    total_weight = 0
    total_point = 0
    tbottle_weight = 0
    tcan_weight = 0
    bottle_count = 0
    can_count = 0
    global Total_weight_value,Total_point_value,Total_canw_value,Total_bottlew_value,Total_can_value,Total_plastic_value,session_id

    db_module.create_table()
    session_id = db_module.create_session_id()
    created = datetime.now()

    while True:
        result = send_and_receive("readnew") 
        if result:
            weight, matType, errorFlag = result
                
            if errorFlag == 1 and matType == 2:
                total_weight += weight
                can_count += 1
                tcan_weight += weight
                playsound.play_music(music_Hnext)

            if errorFlag == 1 and matType ==1:
               total_weight += weight
               bottle_count += 1
               tbottle_weight += weight
               playsound.play_music(music_Hnext)

            if errorFlag == 0 and weight > 5:
               playsound.play_music(music_Hheavy)
            
   
        if complete_button:
            break
        
        Total_weight_value = total_weight
        Total_point_value = total_point
        Total_canw_value = tcan_weight
        Total_bottlew_value = tbottle_weight
        Total_can_value = can_count
        Total_plastic_value = bottle_count

         # Insert the current values into the database
        modified = datetime.now()
        db_module.insert_or_update_values(can_count, tcan_weight, bottle_count, tbottle_weight,created,modified,session_id)
       

        


def ymain():

    total_weight = 0
    total_point = 0
    tbottle_weight = 0
    tcan_weight = 0
    bottle_count = 0
    can_count = 0
    global Total_weight_value,Total_point_value,Total_canw_value,Total_bottlew_value,Total_can_value,Total_plastic_value,session_id

    db_module.create_table()
    session_id = db_module.create_session_id()
    created = datetime.now()

    while True:
        result = send_and_receive("readnew") 
        if result:
            weight, matType, errorFlag = result
                
            if errorFlag == 1 and matType == 2:
                total_weight += weight
                can_count += 1
                tcan_weight += weight
                playsound.play_music(music_Ynext)

            if errorFlag == 1 and matType ==1:
               total_weight += weight
               bottle_count += 1
               tbottle_weight += weight
               playsound.play_music(music_Ynext)

            if errorFlag == 0 and weight > 5:
               playsound.play_music(music_Yheavy)
            
        
        if complete_button:
            break
        
        Total_weight_value = total_weight
        Total_point_value = total_point
        Total_canw_value = tcan_weight
        Total_bottlew_value = tbottle_weight
        Total_can_value = can_count
        Total_plastic_value = bottle_count

        # Insert the current values into the database
        modified = datetime.now()
        db_module.insert_or_update_values(can_count, tcan_weight, bottle_count, tbottle_weight,created,modified,session_id)


def imain():

    total_weight = 0
    total_point = 0
    tbottle_weight = 0
    tcan_weight = 0
    bottle_count = 0
    can_count = 0
    global Total_weight_value,Total_point_value,Total_canw_value,Total_bottlew_value,Total_can_value,Total_plastic_value,session_id

    db_module.create_table()
    session_id = db_module.create_session_id()
    created = datetime.now()

    while True:
        result = send_and_receive("readnew") 
        if result:
            weight, matType, errorFlag = result
                
            if errorFlag == 1 and matType == 2:
                total_weight += weight
                can_count += 1
                tcan_weight += weight
                playsound.play_music(music_Inext)

            if errorFlag == 1 and matType ==1:
               total_weight += weight
               bottle_count += 1
               tbottle_weight += weight
               playsound.play_music(music_Inext)

            if errorFlag == 0 and weight > 5:
               playsound.play_music(music_Iheavy)
            
        
        if complete_button:
            break
        
        Total_weight_value = total_weight
        Total_point_value = total_point
        Total_canw_value = tcan_weight
        Total_bottlew_value = tbottle_weight
        Total_can_value = can_count
        Total_plastic_value = bottle_count

        # Insert the current values into the database
        modified = datetime.now()
        db_module.insert_or_update_values(can_count, tcan_weight, bottle_count, tbottle_weight,created,modified,session_id)


#Reset Values Section#
def resetv():
	global Total_weight_value,Total_point_value,Total_canw_value,Total_bottlew_value,Total_can_value,Total_plastic_value
	Total_weight_value = 0
	Total_point_value = 0
	Total_canw_value = 0
	Total_bottlew_value = 0
	Total_can_value = 0
	Total_plastic_value = 0
#Reset Values Section#


@app.route('/')
def main_page():
    resetv()
    return render_template("index.html")

@app.route('/start')
def start_page():
    global complete_button
    complete_button = False
    thread1 = threading.Thread(target=in_sound)
    thread1.start()
    thread = threading.Thread(target=main)
    thread.start()
    return render_template("page2.html")

@app.route('/ystart')
def ystart_page():
    global complete_button
    complete_button = False
    thread1 = threading.Thread(target=in_Ysound)
    thread1.start()
    thread = threading.Thread(target=ymain)
    thread.start()
    return render_template("ypage2.html")

@app.route('/hstart')
def hstart_page():
    global complete_button
    complete_button = False
    thread1 = threading.Thread(target=in_Hsound)
    thread1.start()
    thread = threading.Thread(target=hmain)
    thread.start()
    return render_template("hpage2.html")

@app.route('/istart')
def istart_page():
    global complete_button
    complete_button = False
    thread1 = threading.Thread(target=in_Isound)
    thread1.start()
    thread = threading.Thread(target=imain)
    thread.start()
    return render_template("ipage2.html")

@app.route('/complete')
def complete_page():
    global complete_button
    complete_button = True
    return render_template('page3.html')

@app.route('/ycomplete')
def ycomplete_page():
    global complete_button
    complete_button = True
    return render_template('ypage3.html')

@app.route('/hcomplete')
def hcomplete_page():
    global complete_button
    complete_button = True
    return render_template('hpage3.html')

@app.route('/icomplete')
def icomplete_page():
    global complete_button
    complete_button = True
    return render_template('ipage3.html')

@app.route('/scan')
def scan_page():
    thread1 = threading.Thread(target=in_sounds)
    thread1.start()
    printer.print_it(Total_weight_value,Total_point_value,Total_canw_value,Total_bottlew_value,Total_can_value,Total_plastic_value, session_id)	
    return render_template('page4.html')

@app.route('/yscan')
def yscan_page():
    thread1 = threading.Thread(target=in_Ysounds)
    thread1.start()
    printer.print_it(Total_weight_value,Total_point_value,Total_canw_value,Total_bottlew_value,Total_can_value,Total_plastic_value, session_id)	
    return render_template('ypage4.html')

@app.route('/hscan')
def hscan_page():
    thread1 = threading.Thread(target=in_Hsounds)
    thread1.start()
    printer.print_it(Total_weight_value,Total_point_value,Total_canw_value,Total_bottlew_value,Total_can_value,Total_plastic_value, session_id)	
    return render_template('hpage4.html')

@app.route('/iscan')
def iscan_page():
    thread1 = threading.Thread(target=in_Isounds)
    thread1.start()
    printer.print_it(Total_weight_value,Total_point_value,Total_canw_value,Total_bottlew_value,Total_can_value,Total_plastic_value,session_id)	
    return render_template('ipage4.html')

@app.route('/print')
def print_page():
    thread1 = threading.Thread(target=in_sounds)
    thread1.start()
    printer.print_it(Total_weight_value,Total_point_value,Total_canw_value,Total_bottlew_value,Total_can_value,Total_plastic_value,session_id)
    return render_template('page4.html')

@app.route('/yprint')
def yprint_page():
    thread1 = threading.Thread(target=in_Ysounds)
    thread1.start()
    printer.print_it(Total_weight_value,Total_point_value,Total_canw_value,Total_bottlew_value,Total_can_value,Total_plastic_value, session_id)
    return render_template('ypage4.html')

@app.route('/hprint')
def hprint_page():
    thread1 = threading.Thread(target=in_Hsounds)
    thread1.start()
    printer.print_it(Total_weight_value,Total_point_value,Total_canw_value,Total_bottlew_value,Total_can_value,Total_plastic_value, session_id)
    return render_template('hpage4.html')

@app.route('/iprint')
def iprint_page():
    thread1 = threading.Thread(target=in_Isounds)
    thread1.start()
    printer.print_it(Total_weight_value,Total_point_value,Total_canw_value,Total_bottlew_value,Total_can_value,Total_plastic_value, session_id)
    return render_template('ipage4.html')

@app.route('/stream1')
def stream1():
    return Response(f"data: {Total_weight_value}\n\n", mimetype='text/event-stream')

@app.route('/stream2')
def stream2():
    return Response(f"data: {Total_point_value}\n\n", mimetype='text/event-stream')

@app.route('/stream3')
def stream3():
    return Response(f"data: {Total_plastic_value}\n\n", mimetype='text/event-stream')

@app.route('/stream4')
def stream4():
    return Response(f"data: {Total_can_value}\n\n", mimetype='text/event-stream')

@app.route('/stream5')
def stream5():
    return Response(f"data: {Total_bottlew_value}\n\n", mimetype='text/event-stream')

@app.route('/stream6')
def stream6():
    return Response(f"data: {Total_canw_value}\n\n", mimetype='text/event-stream')




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
