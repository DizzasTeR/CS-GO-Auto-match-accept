# Work in progress

import os
import sys
import random
import pyautogui
from win32gui import GetWindowText, GetForegroundWindow, GetWindowRect
from PIL import Image

debug_mode = True

if debug_mode:
	def debugPrint(*args):
		return print(*args)
else:
	def debugPrint(*args):
		pass

def generate_custom_img(resolution):
	img = Image.open("img/1024x768.png")
	custom = img.resize(resolution)
	custom.save("img/{}x{}.png".format(resolution[0], resolution[1]))

	img.close()
	custom.close()

def run_program():
	print("Monitoring...")
	while(True):
		activeWindow = GetForegroundWindow()
		activeWindowName = GetWindowText(activeWindow)
		if str(activeWindowName).startswith("Counter-Strike") or debug_mode:
			debugPrint("CSGO focused, searching for Accept...")
			activeWindowRect = GetWindowRect(activeWindow)
			width, height = activeWindowRect[2], activeWindowRect[3]
			sample_img = "{}x{}".format(width, height)

			if not os.path.isfile("img/{}.png".format(sample_img)):
				print("Generating a custom image for your game resolution...")
				generate_custom_img((width, height))

			debugPrint("Using image: {}x{}".format(width, height))
			btnAcceptLocation = None
			try:
				btnAcceptLocation = pyautogui.locateOnScreen("img/{}.png".format(sample_img), confidence=0.5)
			except:
				print("An error occured! {}".format(sys.exc_info()[0]))

			debugPrint(btnAcceptLocation)
			if btnAcceptLocation != None:
				print("Accepting...")
				pyautogui.moveTo((btnAcceptLocation.left + btnAcceptLocation.width / 2) + random.randrange(3, 10), (btnAcceptLocation.top + btnAcceptLocation.height / 2) + random.randrange(3, 10))
				pyautogui.click()
		pyautogui.sleep(3)

if __name__ == '__main__':
    run_program()
