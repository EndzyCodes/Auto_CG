'''
This script is used to extract text from an image. It uses the pytesseract library to extract text from an image.
just press space to take a screenshot of the region you want to extract text from.
must be run in the same directory as the image you want to extract text from.
to grab a region to extract text from, press space on top left and top right corners of the region.
'''

import keyboard
import pyautogui
import os
import pytesseract
import pyperclip
from PIL import Image

# pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Mark\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def read_text_from_image(image_path):
    try:
        # Open the image file
        with Image.open(image_path) as img:
            # custom_config = r'-c tessedit_char_whitelist=0123456789+=?'
            digit = pytesseract.image_to_string(img)
            # return digit.strip()
            # text = pytesseract.image_to_string(img)
            # print(digit.strip())
            return digit.strip()
    except Exception as e:
        print(f"Error occurred while reading text from image {image_path}: {e}")
        return ""

def extract_text_from_image(image):
    return pytesseract.image_to_string(image)


positions = []

def on_space_pressed(event):
    global positions
    if event.event_type == keyboard.KEY_DOWN:
        position = pyautogui.position()
        # print(position.x,',', position.y)
        print(f'{position.x}, {position.y}')
        positions.append(position)
        if len(positions) == 2:
            top_left = positions[0]
            bottom_right = positions[1]
            height = abs(top_left[1] - bottom_right[1])
            width = abs(top_left[0] - bottom_right[0])
            top = min(top_left[1], bottom_right[1])
            left = min(top_left[0], bottom_right[0])

            print(f"Captured region: Left={left}, Top={top}, Width={width}, Height={height}")
            positions = []

            # Copy positions to clipboard
            position_text = f"{left}, {top}, {width}, {height}"
            pyperclip.copy(position_text)
            print("Positions copied to clipboard.")

try:
    keyboard.on_press_key('space', on_space_pressed)
    print("Press the space key to capture mouse positions. Press Ctrl + C to exit.")
    keyboard.wait('esc')
except KeyboardInterrupt:
    print("Exiting...")
