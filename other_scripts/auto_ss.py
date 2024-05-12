import os
import time
import pyautogui

def screenshot_regions(regions, output_path):
    # Create the output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

    # Take screenshots of each region
    for i, region in enumerate(regions, start=1):
        x, y, width, height = region
        screenshot_name = f"region_{i}.png"
        screenshot_path = os.path.join(output_path, screenshot_name)

        # Increment the index if the file already exists
        while os.path.exists(screenshot_path):
            i += 1
            screenshot_name = f"region_{i}.png"
            screenshot_path = os.path.join(output_path, screenshot_name)

        # Wait for a moment to ensure the screen is ready
        time.sleep(1)

        # Capture the screenshot
        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        screenshot.save(screenshot_path)
        print(f"Saved screenshot {screenshot_name}")

def scroll(move_mouse_to=(0,0), scroll_count=1, scroll_down=True):

    absolute_x_moveTo = move_mouse_to[0]
    absolute_y_moveTo = move_mouse_to[1]

    pyautogui.moveTo(absolute_x_moveTo, absolute_y_moveTo, duration=0.147)
    time.sleep(1)

    for i in range(scroll_count):
        if scroll_down:
            pyautogui.scroll(-120)
        else:
            pyautogui.scroll(120)
        time.sleep(0.1)

def take_ss():
    # full image
    region_1 = [
        (1321, 126, 105, 133),
        (1441, 127, 105, 131),
        (1563, 127, 105, 128),
        (1683, 128, 108, 132),
        (1319, 280, 109, 130),
        (1440, 281, 108, 133),
        (1564, 282, 104, 127),
        (1682, 281, 106, 132)
    ]

    third_row = [
        (1319, 280, 109, 130),
        (1440, 281, 108, 133),
        (1564, 282, 104, 127),
        (1682, 281, 106, 132)
    ]

    # cropped image  
    region_2 = [
        (1347, 147, 48, 56),
        (1464, 148, 55, 50),
        (1581, 154, 67, 43),
        (1706, 153, 64, 49),
        (1344, 311, 53, 38),
        (1466, 307, 52, 44),
        (1591, 313, 55, 40),
        (1715, 307, 44, 41)
    ]
    third_row_two = [
        (1350, 305, 42, 36),
        (1462, 299, 60, 45),
        (1588, 301, 56, 46),
        (1707, 310, 59, 36)
    ]

    output_path_1 = r'C:\Users\Mark\Desktop\AutoPurge_coc\assets\cg_nv\full_imgs'
    output_path_2 = r'C:\Users\Mark\Desktop\AutoPurge_coc\assets\cg_nv'

    # print("FULL IMAGES")
    # screenshot_regions(region_1, output_path_1)
    # scroll((1310, 267), 5)
    # screenshot_regions(third_row, output_path_1)

    # scroll((1310, 267), 5, scroll_down=False)

    print("CROPPED IMAGES")
    screenshot_regions(region_2, output_path_2)
    scroll((1310, 267), 5)
    screenshot_regions(third_row_two, output_path_2)

if __name__ == "__main__":

    take_ss()