import pyautogui
import time
from .window_utils import (
    get_window_rect,
    get_window_handle,
    window_title
)
from .image_detection import (
    check_image_presence,
    click_random_within_image
)
from .click_utils import do_click
from .logging_utils import setlog

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

def switch_acc(assets_path, acc_num=0):

    settings_img = assets_path + '\\mv_assets\\settings.png'
    switch_acc_btn_img = assets_path +  '\\mv_assets\\switch_acc_btn.png'
    account_indicator_img = assets_path + '\\mv_assets\\accounts_indicator.png'

    get_window_handle(window_title)

    if (settings_btn_location := check_image_presence(settings_img, confidence=0.8)):
        click_random_within_image(settings_btn_location)
        setlog("Clicked settings", "info")
        time.sleep(2)
        if (switch_acc_btn_location := check_image_presence(switch_acc_btn_img, confidence=0.8)):
            click_random_within_image(switch_acc_btn_location)
            setlog("Clicked switch account", "info")
        else:
            setlog("Switch account button not found", "error")
            do_click(606, 142) # just click it
    else:
        setlog("Settings button not found", "error")

    while not (account_indicator_location := check_image_presence(account_indicator_img, confidence=0.8)):
        time.sleep(0.1)
    setlog("Accounts window found", "info")

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
    while (switch_acc_btn_location := check_image_presence(switch_acc_btn_img, confidence=0.8)):
        time.sleep(0.1)
    setlog("switch account button is gone", "info")
