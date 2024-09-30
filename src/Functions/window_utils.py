import pygetwindow as gw
import pyautogui
import time
from ..config import window_title
# from ..Features.attack.army_camp import is_army_btn_visible
from .logging_utils import setlog

window_rect = ()

def get_window_rect(window_title, debug=False):
    global window_rect

    window_handle = get_window_handle(window_title) # bring window to foreground
    window_rect1 = gw.getWindowsWithTitle(window_title)[0].box  # get window rectangle using pygetwindow
    # print(window_rect1)
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
        x = 1013
        y = 38
        width = 898
        height = 535
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

def launch_coc(assets_path):
    if is_coc_open():
        return

    setlog("Launching Emulator...", 'info')
    launch_clash_of_clans_on_google_play_games()
    time.sleep(4)
    setlog("Set window size of Emulator", 'info')
    set_window_size(window_name='launcher')
    time.sleep(4)
    coc_icon_img = assets_path + '\\coc_icon.png'
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

    # is_army_btn_visible()

    return True

def print_coc_window_size():
    try:
        # Find the Clash of Clans window
        coc_window = gw.getWindowsWithTitle(window_title)[0]

        # Get the window size
        width = coc_window.width
        height = coc_window.height

        # Print the size
        setlog(f"Clash of Clans window size:", "info")
        setlog(f"Width: {width} pixels", "info")
        setlog(f"Height: {height} pixels", "info")

        return width, height
    except IndexError:
        setlog(f"Window with title '{window_title}' not found.", "error")
        return None
    except Exception as e:
        setlog(f"An error occurred: {str(e)}", "error")
        return None
def set_coc_window_size(width=1351, height=789):
    # set_coc_window_size(1173, 689)
    try:
        # Find the Clash of Clans window
        coc_window = gw.getWindowsWithTitle(window_title)[0]

        # Get the current position
        current_left = coc_window.left
        current_top = coc_window.top

        # Set the new size
        coc_window.resizeTo(width, height)

        # Move the window to ensure it's in the same position after resizing
        coc_window.moveTo(current_left, current_top)

        # Verify the new size
        new_width = coc_window.width
        new_height = coc_window.height

        if new_width == width and new_height == height:
            setlog(f"Clash of Clans window resized successfully", "success")
            setlog(f"New width: {new_width} pixels", "info")
            setlog(f"New height: {new_height} pixels", "info")
        else:
            setlog(f"Resize operation completed, but final size is different", "warning")
            setlog(f"Actual width: {new_width} pixels", "info")
            setlog(f"Actual height: {new_height} pixels", "info")

        return new_width, new_height
    except IndexError:
        setlog(f"Window with title '{window_title}' not found.", "error")
        return None
    except Exception as e:
        setlog(f"An error occurred while resizing: {str(e)}", "error")
        return None
