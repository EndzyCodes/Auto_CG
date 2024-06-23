import pygetwindow as gw
import pyautogui
import time
import win32gui
import pyperclip

# This script gets the rectangle coordinates of a specified window
# It then searches for an image within that window rectangle
# The window rectangle is used to define the search region for the image

window_title = "Clash of Clans"  # window title
window_rect=()

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

def get_region_within_window(image_path, confidence=0.8, timeout=10):
    window_rect = get_window_rect(window_title)
    if not window_rect:
        return False

    try:
        start_time = time.time()
        while time.time() - start_time < timeout:
            # Perform the image search within the window region
            result = pyautogui.locateOnScreen(image_path, confidence=confidence, region=window_rect)
            if result is not None:
                # Calculate the coordinates relative to the window
                final_x = result.left - window_rect[0]
                final_y = result.top - window_rect[1]
                final_width = result.width
                final_height = result.height
                # Copy the region coordinates to clipboard
                region_coordinates = f'{final_x}, {final_y}, {final_width}, {final_height}'
                pyperclip.copy(region_coordinates)
                print(f"Found image at: {region_coordinates}")
                # Move the mouse to the center of the found image
                pyautogui.moveTo(result.left + result.width / 2, result.top + result.height / 2)
                return True
            else:
                time.sleep(0.1)

        return False

    except KeyboardInterrupt:
        print("\nScript stopped.")
    except Exception as e:
        print(f"Error: {e}")
        return False

import pyperclip

def get_window_location_and_size(window_title = ''):
    """
    ​<light>Retrieves the location (x, y) and size (width, height) of a window, and copies the coordinates to the clipboard.</light>

    Parameters:
    window_title (str): The title of the window to get the location and size for.
    """
    # Get the window object
    window = gw.getWindowsWithTitle(window_title)[0]

    # Get the window's location and size
    x = window.left
    y = window.top
    width = window.width
    height = window.height

    # Format the coordinates as a string
    coords_str = f"({x}, {y}, {width}, {height})"

    # Copy the coordinates to the clipboard
    pyperclip.copy(coords_str)

if __name__ == "__main__":

    img = r'C:\Users\fastl\OneDrive\Documents\GitHub\EndzyCodes\Auto_CG\assets\test\damage_percentage.png'

    get_region_within_window(img)
