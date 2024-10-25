from flask import Flask, render_template, Response
import RPi.GPIO as GPIO
import threading
from time import sleep
import time
import sys
import math
from datetime import datetime
import load
# import ultra #temporary fix for faulty load
import servo
import sound
import printer
import ebuka_module
app = Flask(__name__)

servo.setAngle(90)

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
GPIO.output(16, GPIO.LOW)
#GPIO21 is set as input fot Metal detector(Pull up resistor is used as the metal outputs low volatge as signal
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO 16 is set as output for the Crusher relay
def crusher():
    #Turn on crusher
    GPIO.output(16, GPIO.HIGH)
    #crusher to run for 3 seconds
    time.sleep(7)
    #Turn off crusher
    GPIO.output(16, GPIO.LOW)
    

music_welcome = "/home/ecounido24/Downloads/welcome.mp3"
music_next = "/home/ecounido24/Downloads/next.mp3"
music_complete = "/home/ecounido24/Downloads/complete.mp3"
music_heavy = "/home/ecounido24/Downloads/heavy.mp3"
music_Hwelcome = "/home/ecounido24/Downloads/Hwelcome.mp3"
music_Hnext = "/home/ecounido24/Downloads/Hnext.mp3"
music_Hcomplete = "/home/ecounido24/Downloads/Hcomplete.mp3"
music_Hheavy = "/home/ecounido24/Downloads/Hheavy.mp3"
music_Iwelcome = "/home/ecounido24/Downloads/Iwelcome.mp3"
music_Inext = "/home/ecounido24/Downloads/Inext.mp3"
music_Icomplete = "/home/ecounido24/Downloads/Icomplete.mp3"
music_Iheavy = "/home/ecounido24/Downloads/Iheavy.mp3"
music_Ywelcome = "/home/ecounido24/Downloads/Ywelcome.mp3"
music_Ynext = "/home/ecounido24/Downloads/Ynext.mp3"
music_Ycomplete = "/home/ecounido24/Downloads/Ycomplete.mp3"
music_Yheavy = "/home/ecounido24/Downloads/Yheavy.mp3" 
start_button = 0
complete_button = False
print_button = 0
Total_weight_value = 0
Total_point_value = 0
Total_canw_value = 0
Total_bottlew_value = 0
Total_can_value = 0
Total_plastic_value = 0
def main():
	
    total_weight = 0
    total_point = 0
    tbottle_weight = 0
    tcan_weight = 0
    bottle_count = 0
    can_count = 0
    global Total_weight_value,Total_point_value,Total_canw_value,Total_bottlew_value,Total_can_value,Total_plastic_value
    
    ebuka_module.create_table()
    session_id = ebuka_module.create_session_id()
    created = datetime.now()

    while True:
        # servo.setAngle(74)
	
        x = load.measure()
        if x > 5 and x < 60:
            
            if GPIO.input(21) == True:
                time.sleep(2)
                weight = load.measure()
                # print("Can   measured weight:", weight)
                total_weight += weight
                total_point += 3*weight
                tcan_weight += weight
                can_count += 1
                #servo.can_bottle()
                servo.setAngle(35)
                time.sleep(2)
                servo.setAngle(90)
                thread1 = threading.Thread(target=crusher)
                thread1.start()

				
            else:
                time.sleep(2)
                weight = load.measure()
                # print("Plastic measured weight:", weight)
                total_weight += weight
                total_point += 1*weight
                tbottle_weight += weight
                bottle_count += 1
                #servo.plastic_bottle()
                servo.setAngle(155)
                time.sleep(2)
                servo.setAngle(90)
                thread1 = threading.Thread(target=crusher)
                thread1.start()
			#Plays sound to insert next bottle
            sound.play_music(music_next)
        elif x > 99:
            sound.play_music(music_heavy)
        if complete_button:
            print("completed")
            break
        Total_weight_value = total_weight
        Total_point_value = total_point
        Total_canw_value = tcan_weight
        Total_bottlew_value = tbottle_weight
        Total_can_value = can_count
        Total_plastic_value = bottle_count

        # Insert the current values into the database
        modified = datetime.now()
        ebuka_module.insert_values(can_count, tcan_weight, bottle_count, tbottle_weight,created,modified,session_id)
    # print("Total measured weight:", Total_weight_value, "Total Point:", Total_point_value,"Total Can weight:", Total_canw_value, "Total bottle weight:", Total_bottlew_value,"Total Can:", Total_can_value, "Total bottle:", Total_plastic_value)

def hmain():
	
    total_weight = 0
    total_point = 0
    tbottle_weight = 0
    tcan_weight = 0
    bottle_count = 0
    can_count = 0
    global Total_weight_value,Total_point_value,Total_canw_value,Total_bottlew_value,Total_can_value,Total_plastic_value
    while True:
        # servo.setAngle(74)
        x = load.measure()
        if x > 5 and x < 60:
            
            if GPIO.input(21) == True:
                time.sleep(2)
                weight = load.measure()
                # print("Can   measured weight:", weight)
                total_weight += weight
                total_point += 3*weight
                tcan_weight += weight
                can_count += 1
                #servo.can_bottle()
                servo.setAngle(35)
                time.sleep(2)
                servo.setAngle(90)
                thread1 = threading.Thread(target=crusher)
                thread1.start()

				
            else:
                weight = load.measure()
                # print("Plastic measured weight:", weight)
                total_weight += weight
                total_point += 1*weight
                tbottle_weight += weight
                bottle_count += 1
                #servo.plastic_bottle()
                servo.setAngle(155)
                time.sleep(2)
                servo.setAngle(90)
                thread1 = threading.Thread(target=crusher)
                thread1.start()
			#Plays sound to insert next bottle
            sound.play_music(music_Hnext)
        elif x > 99:
            sound.play_music(music_Hheavy)
        if complete_button:
            print("complted")
            break
        Total_weight_value = total_weight
        Total_point_value = total_point
        Total_canw_value = tcan_weight
        Total_bottlew_value = tbottle_weight
        Total_can_value = can_count
        Total_plastic_value = bottle_count
    # print("Total measured weight:", Total_weight_value, "Total Point:", Total_point_value,"Total Can weight:", Total_canw_value, "Total bottle weight:", Total_bottlew_value,"Total Can:", Total_can_value, "Total bottle:", Total_plastic_value)
def imain():
	
    total_weight = 0
    total_point = 0
    tbottle_weight = 0
    tcan_weight = 0
    bottle_count = 0
    can_count = 0
    global Total_weight_value,Total_point_value,Total_canw_value,Total_bottlew_value,Total_can_value,Total_plastic_value
    while True:
        # servo.setAngle(74)
        x = load.measure()
        if x > 5 and x < 60:
            
            if GPIO.input(21) == True:
                weight = load.measure()
                # print("Can   measured weight:", weight)
                total_weight += weight
                total_point += 3*weight
                tcan_weight += weight
                can_count += 1
                #servo.can_bottle()
                servo.setAngle(35)
                time.sleep(2)
                servo.setAngle(90)
                thread1 = threading.Thread(target=crusher)
                thread1.start()

				
            else:
                weight = load.measure()
                # print("Plastic measured weight:", weight)
                total_weight += weight
                total_point += 1*weight
                tbottle_weight += weight
                bottle_count += 1
                #servo.plastic_bottle()
                servo.setAngle(155)
                time.sleep(2)
                servo.setAngle(90)
                thread1 = threading.Thread(target=crusher)
                thread1.start()
			#Plays sound to insert next bottle
            sound.play_music(music_Inext)
        elif x > 99:
            sound.play_music(music_Iheavy)
        if complete_button:
            print("completed")
            break
        Total_weight_value = total_weight
        Total_point_value = total_point
        Total_canw_value = tcan_weight
        Total_bottlew_value = tbottle_weight
        Total_can_value = can_count
        Total_plastic_value = bottle_count
    # print("Total measured weight:", Total_weight_value, "Total Point:", Total_point_value,"Total Can weight:", Total_canw_value, "Total bottle weight:", Total_bottlew_value,"Total Can:", Total_can_value, "Total bottle:", Total_plastic_value)
def ymain():
	
    total_weight = 0
    total_point = 0
    tbottle_weight = 0
    tcan_weight = 0
    bottle_count = 0
    can_count = 0
    global Total_weight_value,Total_point_value,Total_canw_value,Total_bottlew_value,Total_can_value,Total_plastic_value
    while True:
        # servo.setAngle(74)
        x = load.measure()
        if x > 5 and x < 60:
            
            if GPIO.input(21) == True:
                weight = load.measure()
                # print("Can   measured weight:", weight)
                total_weight += weight
                total_point += 3*weight
                tcan_weight += weight
                can_count += 1
                #servo.can_bottle()
                servo.setAngle(35)
                time.sleep(2)
                servo.setAngle(90)
                thread1 = threading.Thread(target=crusher)
                thread1.start()

				
            else:
                weight = load.measure()
                # print("Plastic measured weight:", weight)
                total_weight += weight
                total_point += 1*weight
                tbottle_weight += weight
                bottle_count += 1
                #servo.plastic_bottle()
                servo.setAngle(155)
                time.sleep(2)
                servo.setAngle(90)
                thread1 = threading.Thread(target=crusher)
                thread1.start()
			#Plays sound to insert next bottle
            sound.play_music(music_Ynext)
        elif x > 99:
            sound.play_music(music_Yheavy)
        if complete_button:
            print("completed")
            break
        Total_weight_value = total_weight
        Total_point_value = total_point
        Total_canw_value = tcan_weight
        Total_bottlew_value = tbottle_weight
        Total_can_value = can_count
        Total_plastic_value = bottle_count
    # print("Total measured weight:", Total_weight_value, "Total Point:", Total_point_value,"Total Can weight:", Total_canw_value, "Total bottle weight:", Total_bottlew_value,"Total Can:", Total_can_value, "Total bottle:", Total_plastic_value)



def in_sound():
	sound.play_music(music_welcome)
def in_Hsound():
	sound.play_music(music_Hwelcome)
def in_Isound():
	sound.play_music(music_Iwelcome)
def in_Ysound():
	sound.play_music(music_Ywelcome)
def in_sounds():
	sound.play_music(music_complete)
def in_Hsounds():
	sound.play_music(music_Hcomplete)
def in_Isounds():
	sound.play_music(music_Icomplete)
def in_Ysounds():
	sound.play_music(music_Ycomplete)
def resetv():
	global Total_weight_value,Total_point_value,Total_canw_value,Total_bottlew_value,Total_can_value,Total_plastic_value
	Total_weight_value = 0
	Total_point_value = 0
	Total_canw_value = 0
	Total_bottlew_value = 0
	Total_can_value = 0
	Total_plastic_value = 0
    
@app.route('/')
def main_page():
	resetv()
    
	return render_template('index.html')

@app.route('/fullbin')
def fullbin_page():
	return render_template('fullbin.html')

	
@app.route('/start')
def start_page():
    global complete_button
    complete_button = False
    thread1 = threading.Thread(target=in_sound)
    thread1.start()
    thread = threading.Thread(target=main)
    thread.start()
    return render_template('page2.html')
@app.route('/complete')
def complete_page():
	global complete_button
	complete_button = True	
	return render_template('page3.html')
@app.route('/scan')
def scan_page():
    thread1 = threading.Thread(target=in_sounds)
    thread1.start()	
    return render_template('page4.html')
@app.route('/print')
def print_page():
    thread1 = threading.Thread(target=in_sounds)
    thread1.start()
    printer.print_it(Total_weight_value,Total_point_value,Total_canw_value,Total_bottlew_value,Total_can_value,Total_plastic_value)
    return render_template('page4.html')
@app.route('/hstart')
def hstart_page():
    global complete_button
    complete_button = False
    thread1 = threading.Thread(target=in_Hsound)
    thread1.start()
    thread = threading.Thread(target=hmain)
    thread.start()
    return render_template('hpage2.html')
@app.route('/hcomplete')
def hcomplete_page():
	global complete_button
	complete_button = True	
	return render_template('hpage3.html')
@app.route('/hscan')
def hscan_page():
    thread1 = threading.Thread(target=in_Hsounds)
    thread1.start()	
    return render_template('hpage4.html')
@app.route('/hprint')
def hprint_page():
    thread1 = threading.Thread(target=in_Hsounds)
    thread1.start()
    printer.print_it(Total_weight_value,Total_point_value,Total_canw_value,Total_bottlew_value,Total_can_value,Total_plastic_value)
    return render_template('hpage4.html')
@app.route('/istart')
def istart_page():
    global complete_button
    complete_button = False
    thread1 = threading.Thread(target=in_Isound)
    thread1.start()
    thread = threading.Thread(target=imain)
    thread.start()
    return render_template('ipage2.html')
@app.route('/icomplete')
def icomplete_page():
	global complete_button
	complete_button = True	
	return render_template('ipage3.html')
@app.route('/iscan')
def iscan_page():
    thread1 = threading.Thread(target=in_Isounds)
    thread1.start()	
    return render_template('ipage4.html')
@app.route('/iprint')
def iprint_page():
    thread1 = threading.Thread(target=in_Isounds)
    thread1.start()
    printer.print_it(Total_weight_value,Total_point_value,Total_canw_value,Total_bottlew_value,Total_can_value,Total_plastic_value)
    return render_template('ipage4.html')
@app.route('/ystart')
def ystart_page():
    global complete_button
    complete_button = False
    thread1 = threading.Thread(target=in_Ysound)
    thread1.start()
    thread = threading.Thread(target=ymain)
    thread.start()
    return render_template('ypage2.html')
@app.route('/ycomplete')
def ycomplete_page():
	global complete_button
	complete_button = True	
	return render_template('ypage3.html')
@app.route('/yscan')
def yscan_page():
    thread1 = threading.Thread(target=in_Ysounds)
    thread1.start()	
    return render_template('ypage4.html')
@app.route('/yprint')
def yprint_page():
    thread1 = threading.Thread(target=in_Ysounds)
    thread1.start()
    printer.print_it(Total_weight_value,Total_point_value,Total_canw_value,Total_bottlew_value,Total_can_value,Total_plastic_value)
    return render_template('ypage4.html')
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
