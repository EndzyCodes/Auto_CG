import pyautogui, time
from ...Functions.logging_utils import setlog
from ...Functions.click_utils import do_click

from ...Functions.window_utils import get_window_rect
from ...Functions.ocr_utils import extract_digit_from_image
from ...config import window_title, assets_path

def is_army_btn_visible(click=False):
    from ...Functions.image_detection import check_image_presence, click_random_within_image
    global assets_path

    img = assets_path + '\\army_btn.png'

    setlog("Waiting for army tab to appear", "info")
    while  not check_image_presence(img, confidence=0.8):
        time.sleep(0.3)

    setlog("Army tab found", "success")
    do_click(867, 262)
    do_click(867, 262)
    do_click(867, 262)
    if click:
        if click_random_within_image(check_image_presence(img, confidence=0.8)):
            time.sleep(1)
            setlog("Clicked on army tab", "success")
            return True
        else:
            setlog("No army tab", "info")
            return False

    return True

def isCampFull(assets_path):
    from ...Functions.image_detection import check_image_presence
    full_camp_img = assets_path + '\\mv_assets\\full_camp.png'
    full_camp2_img = assets_path + '\\mv_assets\\full_camp2.png'
    if check_image_presence(full_camp_img, confidence=0.7, region=(134, 127, 19, 23)) or check_image_presence(full_camp2_img, confidence=0.8):
        setlog("Camp is full", "info")
        return True
    else:
        setlog("Camp is not full", "warning")
        return False

def check_troops_training(assets_path):
    from ...Functions.image_detection import check_image_presence
    # Image of the "Training" text that appears when troops are being trained
    training_indicator_img = assets_path + '\\mv_assets\\training_indicator.png'

    if check_image_presence(training_indicator_img, confidence=0.9):
        # If training indicator is found, look for the time
        time_region = (1180, 680, 100, 30)  # Adjust these coordinates based on where the time appears
        time_img = assets_path + '\\temp\\training_time.png'

        window_rect = get_window_rect(window_title)
        screenshot_region = (
            window_rect[0] + time_region[0],
            window_rect[1] + time_region[1],
            time_region[2],
            time_region[3]
        )

        ss = pyautogui.screenshot(region=screenshot_region)
        ss.save(time_img)

        time_text = extract_digit_from_image(time_img)
        if time_text:
            return f"Troops still training. Remaining time: {time_text}"
        else:
            return "Troops are training, but couldn't read the time."
    else:
        return "No troops are currently training."

def checkArmy(assets_path):
    do_click(46, 435)  # click army tab

    training_status = check_troops_training(assets_path)
    setlog(training_status, "info")

    while not isCampFull(assets_path):
        setlog("Camp is not full", "warning")
        training_status = check_troops_training(assets_path)
        setlog(training_status, "info")
        time.sleep(60)  # Check every minute

    setlog("Camp is full, exit checkArmy()", "info")
    do_click(905, 283)  # click away
    return True
