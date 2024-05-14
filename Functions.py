import pygetwindow as gw
import pyautogui
import time
import win32gui
import random
import logging
import colorlog
import keyboard
import pytesseract
from PIL import Image
from datetime import datetime

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Mark\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'


window_title = "Clash of Clans"  # window title
window_rect=()

#* ----- WINDOW FUNCTIONS -----

def get_window_rect(window_title, debug=False):
    global window_rect

    window_handle = get_window_handle(window_title) # bring window to foreground
    window_rect1 = win32gui.GetWindowRect(window_handle) # get window rectangle

    # check 
    if window_rect == window_rect1:
        if debug: print("Window rect is the same")
    elif window_rect == ():  # if window_rect is not initialized
        window_rect = window_rect1
        if debug: print("Window rect initialized"), print("Window rect:", window_rect)
    elif window_rect != window_rect1:
        if debug: print("Window rect changed, updating window rect")
        window_rect = window_rect1
        if debug: print("Window rect:", window_rect)
    else:
        if debug: print("Window rect not changed")

    # print(window_rect)
    return window_rect
    # example usage to know info rect
    # info, rect = get_window_rect(window_title)
    # print(info)
    # print(f"Window Rect: {rect}")

def get_window_handle(window_title):

    try:
        window = gw.getWindowsWithTitle(window_title)[0]
        window.activate()
        # window_handle = window._hWnd
        return window._hWnd

    except IndexError:
        print(f"Window with title '{window_title}' not found.")
        return None

def get_coc_window(window_title):
    try:
        # Find the window by its title
        window = gw.getWindowsWithTitle("Clash of Clans")[0]
        if window:
            # setlog("Clash of Clans window found.", "info")
            window.activate() # If the window is found, bring it to the front
            return True
            # return window[0]
        else:
            setlog(f"No window with title '{window_title}' found.", "error")
            return False
    except Exception as e:
        print(f"An error occurred: {e}")

#* ----------------------------
# def do_click(x, y):
#     pyautogui.click(x, y)

def random_do_click(x, y, rand_x_range=(5, 15), rand_y_range=(5, 15), clicks = 1, hold_duration_ms=0, debug = False):
    # random_do_click(1792, 290, (20,100), (20,89), 1, random.randint(100,200), debug=True)
    for i in range(clicks):
        # Generate random offsets between 5 and 10 pixels
        random_offset_x = random.randint(*rand_x_range)
        random_offset_y = random.randint(*rand_y_range)

        # Calculate the new x and y coordinates with random offsets
        random_x = x + random_offset_x
        random_y = y + random_offset_y

        if keyboard.is_pressed('q'):
            break

        if debug: # if debug is true then print these
            print("Click: ", i + 1) # print current click, + 1 to start counting on 1 and not start 0
            print("Clicking at coords:", random_x, random_y)
            print("offsets: ", random_offset_x, random_offset_y)
            print("Hold duration: ", hold_duration_ms)

        pyautogui.mouseDown(random_x, random_y)
        time.sleep(hold_duration_ms / 1000)
        pyautogui.mouseUp()

def click_close():
    close_btn_img_path = r'C:\Users\Mark\Desktop\coc\Images\close_btn.png'
    close_btn_present = check_image_presence(close_btn_img_path, confidence=0.8)
    if close_btn_present: 
        click_random_within_image(close_btn_present)
    else: 
        print("Close button not found.")

def do_click(relative_x, relative_y, click_duration=0.075, move_duration=0.104, delay_before_click=0.112, random_click = False, debug=False, click_hold=False):

    window_rect = get_window_rect(window_title)
    # print(window_rect)
    # print(window_rect[0], window_rect[1])

    # get_coc_window(window_title)
    if click_duration == 0.075:
        click_duration = random.uniform(0.075, 0.123)
    else: 
        click_duration = random.uniform(0.075, click_duration)
    if move_duration == 0.104:
        move_duration = random.uniform(0.104, 0.217)
    if delay_before_click == 0.112:
        delay_before_click = random.uniform(0.112, 0.234)

    # absolute_x = window_rect[0] + relative_x
    # absolute_y = window_rect[1] + relative_y

    offset_x = relative_x + random.randint(-3,5)
    offset_y = relative_y + random.randint(-3,5)
    absolute_x = window_rect[0] + offset_x
    absolute_y = window_rect[1] + offset_y

    if click_hold:
        pyautogui.moveTo(absolute_x, absolute_y, duration=move_duration)
        pyautogui.mouseDown()
        time.sleep(1.5)
        pyautogui.mouseUp()
    else:
        pyautogui.click(absolute_x, absolute_y, duration=move_duration)

    # return True
    # try:
    #     if not random_click:
    #         absolute_x = window_rect[0] + relative_x
    #         absolute_y = window_rect[1] + relative_y
    #         # print(relative_x, relative_y)

    #         pyautogui.click(absolute_x, absolute_y, duration=move_duration)  # Move gradually to the target
    #         # if debug:
    #         # time.sleep(delay_before_click)
    #         # pyautogui.mouseDown()
    #         # time.sleep(click_duration)
    #         # pyautogui.mouseUp()
    #         return True
    #         # if debug:
    #         #     print(f"Clicked at ({relative_x}, {relative_y})" + " Random click:", random_click)

    #     else:
    #         offset_x = relative_x + random.randint(-3,6)
    #         offset_y = relative_y + random.randint(-3,6)
    #         absolute_x = window_rect[0] + offset_x
    #         absolute_y = window_rect[1] + offset_y

    #         pyautogui.moveTo(absolute_x, absolute_y, duration=move_duration)  # Move gradually to the target
    #         time.sleep(delay_before_click)
    #         pyautogui.mouseDown()
    #         time.sleep(click_duration)
    #         pyautogui.mouseUp()
    #         if debug:
    #             print(f"Original Coords: ({relative_x}, {relative_y})")
    #             print(f"Clicked at ({offset_x}, {offset_y})" + " Random click:", random_click)
    #         return True
    #     # return False

    # except KeyboardInterrupt:
    #     print("\nScript stopped.")
    #     return False

def scroll_to_zoom(move_mouse_to=(0,0), scroll_count=1, zoom_out=True):
    # use case: scroll_to_zoom((716, 117), 10, zoom_out=False) # zoom in 10 times, remove zoom_out=False to zoom out
    window_rect = get_window_rect(window_title)

    offset_x = move_mouse_to[0] + random.randint(-3,5)
    offset_y = move_mouse_to[1] + random.randint(-3,5)
    absolute_x_moveTo = window_rect[0] + offset_x
    absolute_y_moveTo = window_rect[1] + offset_y

    # absolute_x_moveTo = window_rect[0] + move_mouse_to[0]
    # absolute_y_moveTo = window_rect[1] + move_mouse_to[1]

    pyautogui.moveTo(absolute_x_moveTo, absolute_y_moveTo, duration=0.147)
    time.sleep(1)
    if zoom_out:
        setlog("Zooming out", "info")
    else:
        setlog("Zooming in", "info")
    for i in range(scroll_count):
        if zoom_out:
            pyautogui.scroll(-120)
        else:
            pyautogui.scroll(120)
        time.sleep(0.1)

def scroll(move_mouse_to=(0,0), scroll_count=1, scroll_down=True):
    # use case: scroll_to_zoom((716, 117), 10, zoom_out=False) # zoom in 10 times, remove zoom_out=False to zoom out
    window_rect = get_window_rect(window_title)

    absolute_x_moveTo = window_rect[0] + move_mouse_to[0]
    absolute_y_moveTo = window_rect[1] + move_mouse_to[1]

    pyautogui.moveTo(absolute_x_moveTo, absolute_y_moveTo, duration=0.147)
    time.sleep(1)
    if scroll_down:
        setlog("Scrolling down...", "info")
    else:
        setlog("Scrolling up...", "info")
    for i in range(scroll_count):
        if scroll_down:
            pyautogui.scroll(-120)
        else:
            pyautogui.scroll(120)
        time.sleep(0.1)

def click_drag(x, y, x_moveTo, y_moveTo, duration=0.175, debug=False):
    # use case: click_drag(716, 117, 419, 376)
    window_rect = get_window_rect(window_title)

    absolute_x = window_rect[0] + x
    absolute_y = window_rect[1] + y

    absolute_x_moveTo = window_rect[0] + x_moveTo
    absolute_y_moveTo = window_rect[1] + y_moveTo

    if debug: setlog(f"Moving from ({x}, {y}) to ({x_moveTo}, {y_moveTo})", "info")

    pyautogui.moveTo(absolute_x, absolute_y, duration=duration)
    time.sleep(0.5)
    pyautogui.mouseDown()
    pyautogui.moveTo(absolute_x_moveTo, absolute_y_moveTo, duration=0.220)
    pyautogui.mouseUp()

def move_to(x,y):
    window_rect = get_window_rect(window_title)
    absolute_x = window_rect[0] + x
    absolute_y = window_rect[1] + y

    pyautogui.moveTo(absolute_x, absolute_y)

#* ---- MAIN VILLAGE FUNCTIONS ----

#* ----------------------------

#* ----- SWITCH ACCOUNT FUNCTIONS -----
def scroll_acc_switch(move_mouse_to=(0,0), scroll_count=1, scroll_down=False, scroll_up=False):
    # use case: scroll_to_zoom((716, 117), 10, zoom_out=False) # zoom in 10 times, remove zoom_out=False to zoom out
    window_rect = get_window_rect(window_title)

    absolute_x_moveTo = window_rect[0] + move_mouse_to[0]
    absolute_y_moveTo = window_rect[1] + move_mouse_to[1]

    pyautogui.moveTo(absolute_x_moveTo, absolute_y_moveTo, duration=0.147)
    time.sleep(1)
    for i in range(scroll_count):
        if scroll_down:
            pyautogui.scroll(-120)
        elif scroll_up:
            pyautogui.scroll(120)
        time.sleep(0.1)

def switch_acc(acc_num=0):

    get_window_handle(window_title)
    if do_click(901, 425):
        setlog("Click settings", "info")
        time.sleep(0.5)
        if do_click(606, 141): # click switch account
            setlog("Click switch account", "info")
        else:
            setlog("Switch account button not found", "error")

    time.sleep(2.5)

    if acc_num <= 4:
        time.sleep(0.3)
        do_click(735, 300 + (acc_num - 1) * 70) # PEMDAS method

    elif acc_num <= 8 and acc_num > 4:
        scroll_acc_switch((745, 338), 6, scroll_down=True)
        time.sleep(0.3)
        do_click(735, 300 + (acc_num - 5) * 70)

    elif acc_num <= 12 and acc_num > 8:
        scroll_acc_switch((745, 338), 12, scroll_down=True)
        do_click(735, 300 + (acc_num - 9) * 70)

    elif acc_num <= 16 and acc_num > 12:
        scroll_acc_switch((745, 338), 18, scroll_down=True)
        do_click(735, 283 + (acc_num - 13) * 70)

    elif acc_num <= 20 and acc_num > 16:
        scroll_acc_switch((745, 338), 24, scroll_down=True)
        do_click(733, 283 + (acc_num - 17) * 70)

    elif acc_num == 21:
        scroll_acc_switch((745, 338), 30, scroll_down=True)
        time.sleep(0.3)
        do_click(733, 393)

    setlog("Switching to account " + str(acc_num), "success")
    time.sleep(2)

#* ----------------------------


#* ----- OCR FUNCTIONS -----
def click_if_pixel_matches(pixel_x, pixel_y, expected_color, tolerance=10, click_duration=0.75, move_duration=0.104, called_from="", random_click = False, debug=False,):
    # Function to click if the pixel color matches the expected color within the specified window
    if click_duration == 0.075:
        click_duration = random.uniform(0.075, 0.123)
    if move_duration == 0.104:
        move_duration = random.uniform(0.104, 0.217)

    # window_handle = get_window_handle(window_title)
    window_rect = get_window_rect(window_title)

    try:
        # get the specified window's current position and size on the screen
        # window_rect = win32gui.GetWindowRect(window_handle)
        if not random_click:    
            # calculate absolute coordinates
            absolute_x = window_rect[0] + pixel_x
            absolute_y = window_rect[1] + pixel_y
            # check if the pixel color matches the expected color
            if pyautogui.pixelMatchesColor(absolute_x, absolute_y, expected_color, tolerance=tolerance):
                pyautogui.moveTo(x=absolute_x, y=absolute_y, duration=move_duration)  
                pyautogui.mouseDown()
                time.sleep(click_duration)
                pyautogui.mouseUp()
                if debug:
                    print(f"Clicked at pixel location ({pixel_x}, {pixel_y}) due to color match.")
                return True
            else:
                setlog(f"Pixel color at ({pixel_x}, {pixel_y}) does not match the expected color. Called from:{called_from}", "error")

        else:
            rand_pix_x = pixel_x + random.randint(-5,10)
            rand_pix_y = pixel_y + random.randint(-5,10)
            absolute_x = window_rect[0] + rand_pix_x
            absolute_y = window_rect[1] + rand_pix_y
            if pyautogui.pixelMatchesColor(absolute_x, absolute_y, expected_color, tolerance=tolerance):
                pyautogui.moveTo(x=absolute_x, y=absolute_y, duration=move_duration)  
                pyautogui.mouseDown()
                time.sleep(click_duration)
                pyautogui.mouseUp()
                if debug:
                    print(f"Original Coords: ({pixel_x}, {pixel_y})")
                    print(f"Clicked at ({rand_pix_x}, {rand_pix_y})" + " Random click:", random_click)
                return True
            else:
                setlog(f"Pixel color at ({pixel_x}, {pixel_y}) does not match the expected color. Called from:{called_from}", "error")
                return False
    except KeyboardInterrupt:
        print("\nScript stopped.")

def pixel_match(pixel_x, pixel_y, expected_color, tolerance=10, move_duration=0.104,  called_from="", debug_txt="", debug=False,):
    # function call example: pixel_match(333, 157, (13, 91, 130))

    window_rect = get_window_rect(window_title)

    try:
        # calculate absolute coordinates
        absolute_x = window_rect[0] + pixel_x
        absolute_y = window_rect[1] + pixel_y
        # check if the pixel color matches the expected color
        if pyautogui.pixelMatchesColor(absolute_x, absolute_y, expected_color, tolerance=tolerance):
            # if debug:
            pyautogui.moveTo(x=absolute_x, y=absolute_y, duration=move_duration)
            if debug: setlog(f"Pixel matched at ({pixel_x}, {pixel_y}), {debug_txt}", "success")
            return True
        else:
            if debug:
                pyautogui.moveTo(x=absolute_x, y=absolute_y, duration=move_duration)
                setlog(f"Pixel color at ({pixel_x}, {pixel_y}) does not match the expected color.", "error")
            return False
    except (KeyboardInterrupt, ):
        print("\nScript stopped.")

def click_on_image(image_path, confidence=0.8, timeout=10, is_donate = False, click_duration=0.075, move_duration=0.104, click=False, debug=False):
    # Function to click on the found image within the specified window handle

    if click_duration == 0.075: # if click_duration is default then randomize it
        click_duration = random.uniform(0.075,0.123)
    if move_duration == 0.104:
        move_duration = random.uniform(0.104, 0.217)

    if is_donate: # do not randomize from 0.1 when is_donate is True, only randomize if not donating
        pass 
    # if user specify a click_duration then randomize it from default value to user specified value
    if click_duration != 0.1 and not is_donate:
        click_duration = random.uniform(0.1, click_duration)
        # if debug: print(f"click_duration: {click_duration}")

    window_rect = get_window_rect(window_title)

    try:
        start_time = time.time()
        while time.time() - start_time < timeout: # timeout=10 is 10 seconds, run this while loop for 10 seconds only
            # Perform the image search within the window
            result = pyautogui.locateOnScreen(image_path, confidence=confidence, region=window_rect)

            if result is not None:
                # Click on the center of the found image
                rand_offset_x = random.randint(-7, 10)
                rand_offset_y = random.randint(-7, 10)
                
                final_x = result.left + result.width // 2 + rand_offset_x
                final_y = result.top + result.height // 2 + rand_offset_y
                pyautogui.moveTo(x=final_x, y=final_y, duration=move_duration)

                if debug: print(final_x, final_y)

                if click: #TODO remove click parameter after testing images
                    pyautogui.mouseDown()
                    time.sleep(click_duration)
                    pyautogui.mouseUp()
                if debug: print(f"Clicked at ({result.left + result.width // 2 + rand_offset_x}, {result.top + result.height // 2 + rand_offset_y})")

                return True
            else:
                time.sleep(0.100)

        return False

    except KeyboardInterrupt:
        setlog("\nScript stopped.", "error")
    except Exception as e:
        if debug:
            setlog(f"Image not found", "error")

def click_random_within_image(image_location, hold_ms=0.247, click=1, debug=False):
    try:
        if image_location:
            x, y, width, height = image_location
            for i in range(click):
                random_x = random.randint(x, x + width)
                random_y = random.randint(y, y + height)

                if debug:
                    print("Clicking at:", random_x, random_y, "Hold duration:", hold_ms, "Click:", i + 1)

                pyautogui.moveTo(random_x, random_y, duration=0.174)
                pyautogui.mouseDown()
                time.sleep(hold_ms)
                pyautogui.mouseUp()

            return True
        else:
            # setlog("Image not found.", "error")
            return False
    except pyautogui.ImageNotFoundException:
        # setlog("Image not found.", "error")
        return False

def find_image(image_path, confidence=0.8, timeout=10, debug=False):
    # Function for finding image within the specified window handle

    window_rect = get_window_rect(window_title)

    try:
        start_time = time.time()
        while time.time() - start_time < timeout: # timeout=10 is 10 seconds, run this while loop for 10 seconds only
            # Perform the image search within the window
            result = pyautogui.locateOnScreen(image_path, confidence=confidence, region=window_rect)

            if result is not None:
                # Click on the center of the found image
                rand_offset_x = random.randint(-7, 10)
                rand_offset_y = random.randint(-7, 10)
                move_duration = random.uniform(0.75, 0.123)
                if debug:
                    pyautogui.moveTo(x=result.left + result.width // 2 + rand_offset_x, y=result.top + result.height // 2 + rand_offset_y, duration=move_duration)
                    print(f"image found at ({result.left + result.width // 2 + rand_offset_x}, {result.top + result.height // 2 + rand_offset_y})")

                return True
            else:
                time.sleep(0.010) # sleep 10 ms

        return False

    except KeyboardInterrupt:
        print("\nScript stopped.")
    except Exception as e:
        if debug:
            print(f"Image not found")

def check_image_presence(image_path, confidence=0.8, region=None):
    window_rect = get_window_rect(window_title)
    if region is None: 
        region = window_rect
    else: # make user specifed region relative to window_rect if not None
        region = (
            window_rect[0] + region[0],
            window_rect[1] + region[1],
            region[2],
            region[3]
        )
    try:
        image_location = pyautogui.locateOnScreen(image_path, confidence=confidence, region=region)
        return image_location
    except pyautogui.ImageNotFoundException:
        return False

def get_pixel_color(x, y):
    window_rect = get_window_rect(window_title)

    absolute_x = window_rect[0] + x
    absolute_y = window_rect[1] + y
    # Get the pixel color at the specified coordinates
    pixel_color = pyautogui.pixel(absolute_x, absolute_y)
    setlog(f"Pixel Color (RGB): {pixel_color}", "info")
    return pixel_color

def extract_digit_from_image(image_path):
    try:
        image = Image.open(image_path)  # Open the image file
        custom_config = r'-c tessedit_char_whitelist=0123456789'
        digit = pytesseract.image_to_string(image, config=custom_config)  # Extract the digit from the image using OCR
        # digit = pytesseract.image_to_string(image)  # Extract the digit from the image using OCR
        print(digit)
        digit = digit.replace('s', '5').replace('S', '5').replace('i', '1').replace('I', '1').replace('x','')

        digit1 = str(digit)
        # print(digit)
        # return digit  # Return the extracted digit

        if len(digit1) > 7:
            digit1 = digit1[:7]  # Keep only the first 7 digits if more are extracted

        digit2 = ''.join(filter(str.isdigit, digit1))  # Extract only digits from OCR result
        digit3 = digit2.strip()
        print(digit3)
        if digit3.isdigit():  # Check if extracted string is a valid digit
            return int(digit3)
        else:
            return None
    except Exception as e:
        print(f"Error extracting digits from image: {e}")  # Print error message if extraction fails
        return None  # Return None if extraction fails

# def extract_digit_from_image(image_path):
#     try:
#         image = Image.open(image_path)  # Open the image file
#         digit = pytesseract.image_to_string(image, config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789')  # Extract the digit from the image using OCR
#         digit = digit.strip()  # Remove leading and trailing whitespaces
#         digit = digit.replace('s', '5').replace('S', '5')  # Replace 's' and 'S' with '5'
#         return str(digit)
#         # return digit  # Return the extracted digit
#     except Exception as e:
#         print(f"Error extracting digits from image: {e}")  # Print error message if extraction fails
#         return None  # Return None if extraction fails

def find_image_within_window(image_path, confidence=0.8, timeout=10, debug=False):
    # img = r'C:\Users\Mark\Desktop\PyAutomateEmulator\images\troop_cap.png'
    # get_region_within_window(img)
    window_rect = get_window_rect(window_title)

    try:
        start_time = time.time()
        while time.time() - start_time < timeout: # timeout=10 is 10 seconds, run this while loop for 10 seconds only
            # Perform the image search within the window
            result = pyautogui.locateOnScreen(image_path, confidence=confidence, region=window_rect)

            if result is not None:
                # Click on the center of the found image

                final_x = result.left 
                final_y = result.top 
                final_width = result.width
                final_height = result.height

                # print(final_x, final_y, final_width, final_height)

                # pyautogui.moveTo(x=final_x, y=final_y, duration=move_duration)

                # print(final_x, final_y)

                return True
            else:
                time.sleep(0.100)

        return False

    except KeyboardInterrupt:
        setlog("\nScript stopped.", "warning")
    except Exception as e:
        if debug: setlog(f"Image not found", "error")
        return False

# backup - alternative for locating image

# x, y = pyautogui.locateCenterOnScreen(sb_img, confidence=0.8, region=window_rect)
# rx = random.randint(-5, 10)
# ry = random.randint(-5, 10)

# final_rx = x + rx
# final_ry = y + ry

# pyautogui.moveTo(final_rx, final_ry)
# print(f"Clicking at x: {final_rx}, y: {final_ry}")

def ocr_an_image():
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
    
    troop_count_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\test\troop_count.png' 
    ss = pyautogui.screenshot(region=screenshot_region)
    ss.save(troop_count_img)

    troop_count_img = extract_digit_from_image(troop_count_img)
    print(troop_count_img)

#* ------------------------------


#* ---- CLAN GAMES FUNCTION ----

#* ------------------------------


#* ---- BUILDER BASE FUNCTIONS ----

#* ------------------------------


#* ---- FUNCTIONS FOR DEBUGGING ----
# logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%H:%M:%S')
# log_formatter = colorlog.ColoredFormatter(
#     '%(green)s[%(asctime)s]%(reset)s:%(log_color)s %(message)s%(reset)s', datefmt='%H:%M:%S',
#     log_colors={
#         'DEBUG': 'white',
#         'INFO': 'cyan',
#         'WARNING': 'yellow',
#         'ERROR': 'red',
#         'CRITICAL': 'bold_red',
#     }
# )

# # Create a handler with the color formatter
# console_handler = logging.StreamHandler()
# console_handler.setFormatter(log_formatter)

# Set up the root logger with the colored console handler
# logging.root.setLevel(logging.INFO)
# logging.root.addHandler(console_handler)
def get_func_performance(func):
    # function call example: get_func_performance(func_to_run
    start_time = time.time()

    func()

    end_time = time.time()
    runtime = end_time - start_time
    setlog(f"Runtime: {runtime} seconds",'success')

def func_to_run():
    # do_click(312, 54,random_click=True)

    window_rect = get_window_rect(window_title)

    time.sleep(1)

    # clan_chat_tab_img = r'C:\Users\Mark\Desktop\PyAutomateEmulator\images\clan_chat_tab.png'
    # if click_on_image(clan_chat_tab_img, confidence=0.8):
    #     setlog("detected clan chat tab", 'success')
    # else:
    #     setlog("unable to find image", 'error')
    # setlog("test 1", "warning")

    # img = r'C:\Users\Mark\Desktop\PyAutomateEmulator\images\troop_cap.png'
    # get_region_within_window(img)

    region1 = (1049, 129, 90, 21)
    img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\test\gold_loot.png'
    ss_troop_cap = pyautogui.screenshot(region=region1)
    ss_troop_cap.save(img)

    troop_cap_info = extract_digit_from_image(img)
    print
    if troop_cap_info != "45":
        print("True")
        # print(troop_cap_info)
    else:
        # print(troop_cap_info)
        print("false")
    # equation_text = extract_digit_from_image(troop_cap_img_path)

    # if find_image(troop_cap_img_path, confidence=0.8):
    #     print("true")

def get_window_location():
    import pyperclip
    window_title = "Google Play Games Beta"
    """
    Retrieves the current location (x, y) of a window.
    
    Parameters:
    window_title (str): The title of the window to get the location for.
    
    Returns:
    tuple: A tuple containing the x and y coordinates of the window's location.
    """
    # Get the window object
    window = gw.getWindowsWithTitle(window_title)[0]

    # Get the window's current location
    x = window.left
    y = window.top
    print(f'Window location: ({x}, {y})')
    '''copy location to clipboard'''
    pyperclip.copy(f'({x}, {y})')
    return (x, y)

# window_size = (661, 32, 1932, 777)
# terminal_window_size = (-7, 32, 563, 563)
# def set_window_size(window_size):
def set_window_size(window_name = "", noramal_size=False):

    # call the function: set_window_size(window_size)
    # left, top, right, bottom = window_size
    # width = right - left
    # height = bottom - top

    if window_name == "terminal":
        window_title = "Administrator: Desktop"  # Add the window title here
        x = -7
        y = 32
        width = 572
        height = 563
        if noramal_size:
            x = -7
            y = 32
            width = 1013
            height = 563
    elif window_name == "launcher":
        window_title = "Google Play Games beta"
        x = 740
        y = 32
        width = 1184
        height= 639
        window_size = (x, y, width, height)
    elif window_name == "coc":
        window_title = "Clash of Clans"
        x = 1008
        y = 32
        width = 913
        height = 543
        window_size = (x, y, width, height)

    windows = gw.getWindowsWithTitle(window_title)
    if windows:
        window = windows[0]
        window.resizeTo(width, height)
        window.moveTo(x, y)

import subprocess
def launch_clash_of_clans_on_google_play_games():
    """
    Launches the Clash of Clans app using the Google Play Games app for Windows.
    """
    # Path to the Google Play Games app executable
    google_play_games_path = r"C:\Program Files\Google\Play Games\Bootstrapper.exe"

    # Package name of the Clash of Clans app
    # app_package = "com.supercell.clashofclans"

    # Launch the Google Play Games app and start the Clash of Clans app
    # subprocess.run([google_play_games_path, "--launch-package", app_package])
    subprocess.run([google_play_games_path, "--launch-package"])

def close_launcher():
    window_title = "Google Play Games beta"
    """
    Closes the app with the specified window title.

    Parameters:
    window_title (str): The title of the window to close.
    """
    window = gw.getWindowsWithTitle(window_title)
    if window:
        window[0].close()

def is_coc_open():
    """
    Checks if an app with the window title "Clash of Clans" is open.

    Returns:
    bool: True if the app is open, False otherwise.
    """
    window = gw.getWindowsWithTitle("Clash of Clans")
    if window:
        setlog('Clash of Clans is open', 'info')
        return True
    else:
        setlog('Clash of Clans is Close', 'warning')
        return False

def launch_coc():
    from mv_funcs import is_army_btn_visible
    if is_coc_open():
        return

    setlog("Launching Emulator...", 'info')
    launch_clash_of_clans_on_google_play_games()
    time.sleep(4)
    setlog("Set window size of Emulator", 'info')
    set_window_size(window_name='launcher')
    time.sleep(4)
    coc_icon_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\coc_icon.png'
    # while not pyautogui.locateOnWindow(coc_icon_img, 'Google Play Games beta'):
    while not pyautogui.locateOnWindow(coc_icon_img, 'Google Play Games beta'):
        time.sleep(0.2)
        setlog("looking for coc icon...", 'info')

    pyautogui.click(1756, 165) # click coc icon in the launcher
    setlog('Close Launcher', 'info')
    close_launcher()
    setlog('Launching Clash of Clans...', 'info')

    # while Google Play Games beta app is open sleep for 1 sec
    while gw.getWindowsWithTitle("Google Play Games beta"):
        # setlog("waiting for Clash of Clans to load...", 'info')
        time.sleep(2)

    setlog("Set window size of Clash of Clans window", 'info')
    set_window_size(window_name='coc')

    is_army_btn_visible()

    return True

def setup_logging():
    log_formatter = colorlog.ColoredFormatter(
        '%(green)s[%(asctime)s]%(reset)s:%(log_color)s %(message)s%(reset)s', datefmt='%H:%M:%S',
        log_colors={
            'DEBUG': 'white',
            'INFO': 'cyan',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)

    logging.root.setLevel(logging.INFO)
    logging.root.addHandler(console_handler)

def setlog(string, log_level):
    # Define color codes
    color_reset = "\033[0m"
    success_color = "\033[92m" # green
    debug_color = "\033[97m"  # White
    error_color = "\033[91m"  # Red
    info_color = "\033[96m"   # Cyan
    warning_color = "\033[93m"  # Yellow
    heading_color = "\033[94m"
    # other colors
    # \033[30m - Black
    # \033[90m - Bright Black
    # \033[31m - Red
    # \033[91m - Bright Red
    # \033[32m - Green
    # \033[92m - Bright Green
    # \033[33m - Yellow
    # \033[93m - Bright Yellow
    # \033[34m - Blue
    # \033[94m - Bright Blue
    # \033[35m - Magenta/purple
    # \033[95m - Bright Magenta/purple
    # \033[36m - Cyan
    # \033[96m - Bright Cyan
    # \033[37m - White
    # Set color based on log_level
    if log_level == "success":
        color = success_color
    elif log_level == "debug":
        color = debug_color
    elif log_level == "error":
        color = error_color
    elif log_level == "info":
        color = info_color
    elif log_level == "warning":
        color = warning_color
    elif log_level == "heading":
        color = heading_color
    else:
        color = ""  # Default to no color if log_level is not recognized

    # Get current time
    current_time = datetime.now().strftime('%H:%M:%S')

    # Print formatted log message with time
    if log_level == "error":
        print(f"[{current_time}]: {color}[ERROR] {string}{color_reset}")
    else:
        print(f"[{current_time}]: {color}{string}{color_reset}")


setup_logging()

