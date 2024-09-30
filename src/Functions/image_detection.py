import pygetwindow as gw
import pyautogui
import time
import os
import random
from ..Functions.logging_utils import setlog
from ..Functions.window_utils import get_window_rect
from ..config import window_title, assets_path

# window_rect=()

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

def find_multiple_img(img):
    window_rect = get_window_rect(window_title)
    locations = []
    try:
        for loc in pyautogui.locateOnWindow(img, confidence=0.8, title='Clash of Clans'):
            print(f"Found at: {loc}")
            # pyautogui.alert(text=loc, title='WARNING', button='OK')
            locations.append(loc)
            if len(locations) > 10:
                break

        if locations:
            for loc in locations:
                window_rect = get_window_rect(window_title)
                pyautogui.moveTo(loc.left, loc.top)
                time.sleep(1)
        else:
            print("Not Found")
    except Exception as e:
        print(f"An error occurred: {e}")

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

def find_image_in_directory(directory_path, initial_confidence=0.8, min_confidence=0.5):
    #* Usage
    # directory_path = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\bb_assets\attack_btns'
    # matched_image, final_confidence = find_image_in_directory(directory_path)

    # if matched_image:
    #     setlog(f"The matched image is: {matched_image} (Confidence: {final_confidence:.2f})", "info")
    # else:
    #     setlog("No images were matched", "error")
    # Get all image files in the directory
    # ------------------------------------------------------------------

    image_files = [f for f in os.listdir(directory_path) if f.endswith(('.png', '.jpg', '.jpeg'))]

    window_rect = get_window_rect(window_title)
    confidence = initial_confidence

    while confidence >= min_confidence:
        for image_file in image_files:
            image_path = os.path.join(directory_path, image_file)

            try:
                # Attempt to locate the image on screen
                location = pyautogui.locateOnScreen(image_path, confidence=confidence, region=window_rect)

                if location:
                    # Calculate center of the found image
                    center_x = location.left + location.width // 2
                    center_y = location.top + location.height // 2

                    # Move mouse to the center of the found image
                    pyautogui.moveTo(center_x, center_y, duration=0.1)

                    # Print the name of the matched image and the confidence level
                    setlog(f"Found and moved to: {image_file} (Confidence: {confidence:.2f})", "success")

                    return image_file, confidence  # Return the name of the matched image and confidence

            except pyautogui.ImageNotFoundException:
                continue  # Continue to the next image if this one wasn't found

        # If no match found, decrease confidence and try again
        confidence -= 0.1
        setlog(f"No match found. Decreasing confidence to {confidence:.2f}", "warning")

    setlog("No matching images found, even at lowest confidence", "error")
    return None, None

def find_multiple_images_in_directory(directory_path, initial_confidence=0.8, min_confidence=0.5):
    # Usage
    # directory_path = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\bb_assets\attack_btns'
    # matched_image, final_confidence, locations = find_multiple_images_in_directory(directory_path)

    # if matched_image:
    #     setlog(f"The matched image is: {matched_image} (Confidence: {final_confidence:.2f})", "info")
    #     setlog(f"Total matches found: {len(locations)}", "info")
    # else:
    #     setlog("No images were matched", "error")
    # ------------------------------------------------------------------
    image_files = [f for f in os.listdir(directory_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
    window_rect = get_window_rect(window_title)
    confidence = initial_confidence

    while confidence >= min_confidence:
        for image_file in image_files:
            image_path = os.path.join(directory_path, image_file)
            try:
                # First, try to find a single match
                location = pyautogui.locateOnScreen(image_path, confidence=confidence, region=window_rect)
                if location:
                    setlog(f"Found a match for {image_file}. Now searching for multiple instances.", "info")
                    # If a match is found, search for all instances
                    all_locations = list(pyautogui.locateAllOnScreen(image_path, confidence=confidence, region=window_rect))

                    if all_locations:
                        setlog(f"Found {len(all_locations)} matches for {image_file}", "success")
                        for idx, loc in enumerate(all_locations, 1):
                            center_x = loc.left + loc.width // 2
                            center_y = loc.top + loc.height // 2
                            pyautogui.moveTo(center_x, center_y, duration=0.5)
                            setlog(f"Moved to match {idx} at ({center_x}, {center_y})", "info")
                            time.sleep(0.5)  # Short pause between movements

                        return image_file, confidence, all_locations

            except pyautogui.ImageNotFoundException:
                continue

        confidence -= 0.1
        setlog(f"No match found. Decreasing confidence to {confidence:.2f}", "warning")

    setlog("No matching images found, even at lowest confidence", "error")
    return None, None, None
