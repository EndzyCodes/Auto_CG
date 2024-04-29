import pygetwindow as gw
import pyautogui
import time
import win32gui

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
    # img = r'C:\Users\Mark\Desktop\PyAutomateEmulator\images\troop_cap.png'
    # get_region_within_window(img)
    get_window_rect(window_title)

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
                print(f'{final_x}, {final_y}, {final_width}, {final_height}')
                return True
            else:
                time.sleep(0.100)

        return False

    except KeyboardInterrupt:
        print("\nScript stopped.")
    except Exception as e:
        print(f"Image not found")

if __name__ == "__main__":

    img = r'C:\Users\Mark\Desktop\PyAutomateEmulator\images\troop_cap.png'
    get_region_within_window(img)