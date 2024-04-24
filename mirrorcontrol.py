from gpiozero import LED
from gpiozero import MotionSensor
import time

green_led = LED(18)
pir = MotionSensor(4)


motion_detector = False
lights_detector = False

while True:
	pir.wait_for_motion()
	print("Motion Detected")
	motion_detector = True
	print(motion_detector)
	time.sleep(5)
	motion_detector = False
	print(motion_detector)

