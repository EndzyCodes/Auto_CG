from logging_utils import setlog
from window_utils import get_window_rect
import pyautogui
from PIL import Image
import pytesseract
from config import window_title

def extract_digit_from_image(image_path):
    try:
        image = Image.open(image_path)  # Open the image file
        custom_config = r'-c tessedit_char_whitelist=0123456789 -c tessedit_char_blacklist=%'
        digit = pytesseract.image_to_string(image, config=custom_config)  # Extract the digit from the image using OCR
        # digit = pytesseract.image_to_string(image)  # Extract the digit from the image using OCR
        # print(digit)
        digit = digit.replace('s', '5').replace('S', '5').replace('i', '1').replace('I', '1').replace('x','')

        digit1 = str(digit)
        # print(digit)
        # return digit  # Return the extracted digit

        if len(digit1) > 7:
            digit1 = digit1[:7]  # Keep only the first 7 digits if more are extracted

        digit2 = ''.join(filter(str.isdigit, digit1))  # Extract only digits from OCR result
        digit3 = digit2.strip()
        # print(digit3)
        if digit3.isdigit():  # Check if extracted string is a valid digit
            return int(digit3)
        else:
            return None
    except Exception as e:
        print(f"Error extracting digits from image: {e}")  # Print error message if extraction fails
        return None  # Return None if extraction fails

def ocr_an_image(assets_path):
    # Get window rectangle
    window_rect = get_window_rect(window_title)
    if not window_rect:
        print("Failed to get window rectangle.")
        return

    region1 = (150, 148, 28, 20)

    region_x, region_y, region_width, region_height = region1
    screenshot_region = (
        window_rect[0] + region_x,
        window_rect[1] + region_y,
        region_width,
        region_height
    )

    troop_count_img = assets_path + '\\test\\troop_count.png'
    ss = pyautogui.screenshot(region=screenshot_region)
    ss.save(troop_count_img)

    troop_count_img = extract_digit_from_image(troop_count_img)
    print(troop_count_img)
