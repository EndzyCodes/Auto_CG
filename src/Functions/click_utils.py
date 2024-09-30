import pyautogui
import time
import random
import keyboard

from .logging_utils import setlog

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

def click_close(assets_path):
    from .image_detection import check_image_presence, click_random_within_image
    close_btn_img_path = assets_path + '\\test\\close_btn.png'
    close_btn_present = check_image_presence(close_btn_img_path, confidence=0.8)
    if close_btn_present:
        click_random_within_image(close_btn_present)
    else:
        print("Close button not found.")

def do_click(relative_x, relative_y, debug_txt="", click_duration=0.075, move_duration=0.104, delay_before_click=0.112, random_click = True, debug=False, click_hold=False):
    from .window_utils import get_window_rect, window_title
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

    if random_click:
        offset_x = relative_x + random.randint(-2,4)
        offset_y = relative_y + random.randint(-2,4)
        absolute_x = window_rect[0] + offset_x
        absolute_y = window_rect[1] + offset_y
    else:
        absolute_x = window_rect[0] + relative_x
        absolute_y = window_rect[1] + relative_y

    if click_hold:
        pyautogui.moveTo(absolute_x, absolute_y, duration=move_duration)
        setlog(debug_txt, "info")
        pyautogui.mouseDown()
        time.sleep(1.5)
        pyautogui.mouseUp()
    else:
        pyautogui.click(absolute_x, absolute_y, duration=move_duration)
        if debug_txt:
            print(debug_txt)

    return True

def scroll_to_zoom(move_mouse_to=(0,0), scroll_count=1, zoom_out=True):
    # use case: scroll_to_zoom((716, 117), 10, zoom_out=False) # zoom in 10 times, remove zoom_out=False to zoom out
    from .window_utils import get_window_rect, window_title
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
    from .window_utils import get_window_rect, window_title
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
    from .window_utils import get_window_rect, window_title
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
    from .window_utils import get_window_rect, window_title
    window_rect = get_window_rect(window_title)
    absolute_x = window_rect[0] + x
    absolute_y = window_rect[1] + y

    pyautogui.moveTo(absolute_x, absolute_y)
