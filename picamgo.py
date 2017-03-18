import signal
import time, sys
from datetime import datetime
from picamera import PiCamera
from time import sleep
from gpiozero import Button
from signal import pause
from subprocess import check_call

recordButton = Button(22)
shutdownButton = Button(23, hold_time=3)
recording = 0
camera = None

#camera.start_preview()
#for i in range(5):
#    sleep(2)
#    camera.capture('/home/pi/myprojects/picamgo/capture/image%s.jpg' % i)    
#camera.stop_preview()

def signal_handler(signal, frame):
    if camera is not None:
        camera.stop_recording()
        camera.stop_preview()
        camera.close()
    print("bye")
    sys.exit(0)

def shutdown():
	global camera
	print("Shutting down...")
	if camera is not None:
		print("Found camera")
		camera.stop_recording()
		camera.stop_preview()
		camera.close()

	check_call(['sudo','poweroff'])

def record():
	global recording
	global camera
	if recording is 0:
		recording = 1
		camera = PiCamera()
		camera.rotation = 90
		camera.start_preview()
		#camera.start_preview()
		print("Recording...")
		timestamp = datetime.now()
		camera.start_recording('/home/pi/myprojects/picamgo/capture/' + str(timestamp) + '-video.h264')
	else:
		if recording is 1:
			recording = 0
			camera.stop_recording()
			camera.stop_preview()
			camera.close()
			camera = None

recordButton.when_pressed = record		
shutdownButton.when_held = shutdown

pause()

#while True:
#    time.sleep(.3)
#    recordButton.wait_for_press()
#    camera = PiCamera()
#    camera.rotation = 270
#    camera.start_preview()
#    print("Recording...")
#    recordButton.wait_for_release()
#    timestamp = datetime.now()
#    camera.start_recording('/home/pi/myprojects/picamgo/capture/' + str(timestamp) + '-video.h264')
#    recordButton.wait_for_press()
#    print("Stop recording...")
#    recordButton.wait_for_release()
#    camera.stop_recording()
#    camera.stop_preview()
#    camera.close()
