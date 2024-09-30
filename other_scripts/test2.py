from backups.GUI.GUI import ClashOfClansBotGUI
from backups.Functions2 import *
from mv_funcs import is_army_btn_visible, main_village_attack_loop, EdragLoons_strat
from src.features.builder_base.bb_utils import bb_attack_time_limit, bb_attack_loop, attack_BB, bb_return_home, go_to_bb, BB_is_army_btn_visible
from src.features.clan_games.cg_main import purge_challenge, switch_acc_purge, pick_challenge, cg_mode_loop_2, assets_path, cg_mode_loop_3, cg_points_full
# from PyQt6.QtWidgets import QApplication
import pyautogui

"""pixel match the storage bar if full or not"""

def get_cg_points(): # not done yet
    points_region = (138, 464, 46, 22)

    # Get window rectangle
    window_rect = get_window_rect(window_title)
    if not window_rect:
        print("Failed to get window rectangle.")
        return

    # Calculate region within the window
    region_x, region_y, region_width, region_height = points_region
    screenshot_region = (
        window_rect[0] + region_x,
        window_rect[1] + region_y,
        region_width,
        region_height
    )

    ss = pyautogui.screenshot(region=screenshot_region)
    ss.save(r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\test1.png')

    image_path = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\test1.png'
    cg_points = extract_digit_from_image(image_path)

    if cg_points is None:
        print("Failed to extract digits from image.")
    else:
        print(f"Extracted CG points: {cg_points}")

def cg_loop():

    # import keyboard
    count = 1
    start_time = time.time()
    while True:

        if cg_mode_loop_3(assets_path, is_2_camps=True):
            continue
        else:
            setlog("cg_loop - cg_mode_loop_3 returned False", "info")
            setlog("switching to next account", "info")
            break

        if time.time() - start_time >= 60 * 60:  # 2 hours in seconds

            count += 1
            if count > 21:
                count = 1
                switch_acc(count)
                is_army_btn_visible()
            else:
                setlog("time limit reached, switching account...", "info")
                switch_acc(count)
                is_army_btn_visible()
    return True

if __name__ == "__main__":

    # cg_mode_loop_2(assets_path, is_2_camps=True)

    # pick_challenge()
    # cg_loop()

    img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\test\anniv_cake.png'
    for i in pyautogui.locateAllOnScreen(img):
        print(i)
