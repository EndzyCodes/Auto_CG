import pyautogui
import pygetwindow as gw
import keyboard
import pyperclip
import pyperclip
import win32gui

window_title = "Clash of Clans"  # window title
# window_title = "Clash of Clans Bot Configuration"
window_rect=()
def get_window_coordinates(window_title):
    try:
        window = gw.getWindowsWithTitle(window_title)[0]
        if window: print(f"Window with title '{window_title}' found.")
        window.activate()
        return window.left, window.top, window.width, window.height
    except IndexError:
        print(f"Window with title '{window_title}' not found.")
        return None


def get_window_rect(window_title, debug=False):
    global window_rect

    window_handle = get_window_handle(window_title) # bring window to foreground
    window_rect1 = gw.getWindowsWithTitle(window_title)[0].box # get window rectangle

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

def get_coc_window(title):
    try:
        # Find the window by its title
        window = gw.getWindowsWithTitle("Clash of Clans")[0]
        if window:
            print("Clash of Clans window found.")
            window.activate() # If the window is found, bring it to the front
            # return window[0]
        else:
            print(f"No window with title '{title}' found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def track_mouse_coordinates_on_keypress(window_title):
    # window_coords = get_window_coordinates(window_title)

    window_coords = get_window_coordinates(window_title)

    if window_coords is None:
        return

    try:
        while True:
            if keyboard.is_pressed("w"):
                x, y = pyautogui.position()
                on_keypress(x, y, window_coords)
                keyboard.wait("w", suppress=True)  # Wait until the "w" key is released
    except KeyboardInterrupt:
        print("\nTracking stopped.")

def on_keypress(x, y, window_coords):
    window_left, window_top, window_width, window_height = window_coords

    if get_window_rect(window_title):
        # Mouse position is within the specified window
        relative_x = x - window_rect[0]
        relative_y = y - window_rect[1]

        # Get pixel color at the current mouse position
        pixel_color = pyautogui.pixel(x, y)
        rgb_color = (pixel_color[0], pixel_color[1], pixel_color[2])
        hex_color = "#{:02x}{:02x}{:02x}".format(pixel_color[0], pixel_color[1], pixel_color[2])

        # Copy mouse coordinates to clipboard
        coordinates = f"{relative_x}, {relative_y}"
        print(f"Mouse coords: ({coordinates})")
        pyperclip.copy(coordinates)
        print("Mouse coords copied to clipboard")

        print(f"Pixel Color (RGB): {rgb_color}")
        get_pixel_color(relative_x,relative_y)
        print(f"Pixel Color (hex): {hex_color}")
    else:
        # Mouse position is outside the specified window
        print("Mouse position is outside the specified window.")

def get_pixel_color(x, y):
    get_window_rect(window_title)
    absolute_x = window_rect[0] + x
    absolute_y = window_rect[1] + y
    # Get the pixel color at the specified coordinates
    pixel_color = pyautogui.pixel(absolute_x, absolute_y)
    print(f"Pixel Color (RGB): {pixel_color}")
    return pixel_color

if __name__ == "__main__":
    window_title_to_track = "Clash of Clans"  # Replace with your actual window title
    track_mouse_coordinates_on_keypress(window_title_to_track)
    # get_pixel_color(344, 177)
    # get_pixel_color(669, 166)

    # get_pixel_color(331, 166)