from Functions import (
    window_title,
    get_window_rect,
    get_coc_window,
    switch_acc,

    click_random_within_image,
    check_image_presence,
    extract_digit_from_image,
    find_image_within_window,
    find_image,

    do_click,
    click_drag,
    scroll_to_zoom,

    setlog
)
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
# from bb_funcs import bb_attack_loop
import os
import time
import random
import pyautogui
import keyboard
import pygame

assets_path = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets'

def is_army_btn_visible(assets_path, click=False):

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

def is_army_full(assets_path):

    troop_count_img = assets_path + '\\test\\troop_count.png'

    #region = (1263, 697, 118, 30)
    troop_count = extract_digit_from_image(troop_count_img)

    if troop_count is not None:  # Check if troop_count is not None
        if troop_count > 100:
            setlog("Troop count is full!", "warning")
            setlog(f'Troop count: {troop_count}', "warning")
            return True
        else:
            setlog("Troop count is not full", "info")
            setlog(f'Troop count: {troop_count}', "info")
            return False
    else:
        setlog("Failed to extract troop count from image", "error")
        return False  # Return False or handle the error case appropriately

def get_resources_value(resource_target='', target_val=400000):
    global assets_path
    # Define regions and image paths
    regions = {
        'gold': (46, 86, 70, 24),
        'elixir': (43, 108, 72, 24),
        'dark_elixir': (43, 131, 67, 24)
    }

    image_paths = {
        'gold': assets_path + '\\test\\gold_loot.png',
        'elixir': assets_path + '\\test\\elixir_loot.png',
        'dark_elixir': assets_path + '\\test\\dark_elixir_loot.png'
    }

    if resource_target not in regions:
        print("Invalid resource target specified.")
        return

    # Get window rectangle
    window_rect = get_window_rect(window_title)
    if not window_rect:
        print("Failed to get window rectangle.")
        return

    # Calculate region within the window
    region_x, region_y, region_width, region_height = regions[resource_target]
    screenshot_region = (
        window_rect[0] + region_x,
        window_rect[1] + region_y,
        region_width,
        region_height
    )

    # Take screenshot within the specified region of the window
    img_path = image_paths[resource_target]
    ss = pyautogui.screenshot(region=screenshot_region)
    ss.save(img_path)

    # Extract value from the image
    value = extract_digit_from_image(img_path)

    if value is not None:
        if value >= target_val:
            if resource_target == 'gold':
                setlog(f'{resource_target}: {value} - True', "warning")
            elif resource_target == 'elixir':
                setlog(f'{resource_target}: {value} - True', "purple")
            else:
                print(f'{resource_target}: {value} - True')
            return True
        else:
            if resource_target == 'gold':
                setlog(f'{resource_target}: {value} - False', "warning")
            elif resource_target == 'elixir':
                setlog(f'{resource_target}: {value} - False', "purple")
            else:
                print(f'{resource_target}: {value} - False')
            return False
    else:
        print(f'{resource_target}: Error extracting value')
        return None

def isCampFull(assets_path):
    full_camp_img = assets_path + '\\mv_assets\\full_camp.png'
    full_camp2_img = assets_path + '\\mv_assets\\full_camp2.png'
    if check_image_presence(full_camp_img, confidence=0.7, region=(134, 127, 19, 23)) or check_image_presence(full_camp2_img, confidence=0.8):
        setlog("Camp is full", "info")
        return True
    else:
        setlog("Camp is not full", "warning")
        return False

def checkArmy(assets_path):
    do_click(46, 435) # click army tab
    while not isCampFull(assets_path):
        setlog("Camp is not full", "warning")
        time.sleep(1)

    setlog("Camp is full, exit checkArmy()", "info")
    do_click(905, 283) # click away
    return True

def click_drag_troops(x, y, x_moveTo, y_moveTo, duration=0.175, debug=False):
    # use case: click_drag(716, 117, 419, 376)
    window_rect = get_window_rect(window_title)

    # randomize the click position
    offset_x = window_rect[0] + x + random.randint(-3,5)
    offset_y = window_rect[1] + y + random.randint(-3,5)

    # randomize the moveTo position
    absolute_x_moveTo = window_rect[0] + x_moveTo + random.randint(-3,5)
    absolute_y_moveTo = window_rect[1] + y_moveTo + random.randint(-3,5)

    if debug: setlog(f"Moving from ({x}, {y}) to ({x_moveTo}, {y_moveTo})", "info")

    pyautogui.moveTo(offset_x, offset_y, duration=duration)
    # time.sleep(0.5)
    pyautogui.mouseDown()
    time.sleep(0.2)
    pyautogui.moveTo(absolute_x_moveTo, absolute_y_moveTo, duration=1.175)
    time.sleep(0.2)
    pyautogui.mouseUp()

#* ---- ATTACK STRATEGIES ----
def EdragLoons_strat(assets_path):
    # TH14 - 300 army camps space | 8 Edrags 12 Loons | 4 rage 3 Freeze | CC Edrag loons, 2 lightning 1 Freeze
    # TH13 - Same as TH14
    # TH12 - 280 army camps space | 8 Edrags 8 Loons | 4 rage 3 Freeze | CC Edrag loons, 2 lightning
    # TH11 - 260 army camps space | 8 Edrags 4 Loons | same as TH12 | same as TH12

    scroll_to_zoom((300, 353), 10)

    #* ---- BOTTOM-RIGHT DEPLOYMENT ----
    click_drag(636, 314, 460, 200) # Drag to bottom-right
    king_icn_img = assets_path + '\\mv_assets\\king_icon.png'
    queen_icn_img = assets_path + '\\mv_assets\\queen_icon.png'

    if check_image_presence(king_icn_img) and check_image_presence(queen_icn_img):
        setlog("King and Queen are available", "info")
        keyboard.send('q')
        do_click(420, 429, 'Drop King')
        keyboard.send('w')
        do_click(760, 166, 'Drop Queen')
    elif check_image_presence(king_icn_img) and not check_image_presence(queen_icn_img):
        setlog('King is available but Queen is not', 'info')
        keyboard.send('q')
        do_click(420, 429, 'Drop King')
    elif not check_image_presence(king_icn_img) and check_image_presence(queen_icn_img):
        setlog('Queen is available but King is not', 'info')
        keyboard.send('w')
        do_click(760, 166, 'Drop Queen')
    else:
        setlog("King and Queen is not available", 'warning')
        setlog('Using edrag to clear sides...', 'info')
        #* deploy loons on each corner left and right
        keyboard.send('1') # switch to loons
        do_click(420, 429)
        do_click(760, 166)

        time.sleep(2)
        #* deploy edrag on each side
        keyboard.send('2') # switch to edrag
        do_click(420, 429)
        do_click(760, 166)

    #* drop 2 lightning on air sweeper facing 270 degrees
    keyboard.send('d')
    as_270_img = assets_path + '\\mv_assets\\as_270deg.png'
    as_270_img_location = check_image_presence(as_270_img, confidence=0.8)
    if click_random_within_image(as_270_img_location):
        setlog("Dropping lightning on air sweeper facing 270 degrees", "info")
        click_random_within_image(as_270_img_location)  # Click second time

    time.sleep(7)
    #* deploy all loons
    keyboard.send('1') # switch to loons
    loons_drop_points = [
        (538, 364),
        (572, 340),
        (600, 317),
        (636, 290),
        (673, 270),
        (690, 254),
        (564, 351),
        (603, 332),
        (630, 310),
        (668, 276),
        (506, 401),
        (703, 251)
    ]
    random.shuffle(loons_drop_points)
    for point in loons_drop_points:
        do_click(point[0], point[1])

    time.sleep(1)

    #* deploy all edrag
    keyboard.send('2') # switch to edrag
    edrag_drop_points = [
        (524, 369),
        (560, 339),
        (596, 311),
        (632, 283),
        (657, 262),
        (620, 294)
    ]
    random.shuffle(edrag_drop_points)
    for point in edrag_drop_points:
        do_click(point[0], point[1])

    #* Drop warden
    time.sleep(1)
    keyboard.send('e')  # Switch to warden
    warden_drop_points = [
        (636, 290),
        (673, 270),
        (690, 254),
        (564, 351)
    ]
    random.shuffle(warden_drop_points)
    do_click(warden_drop_points[0][0], warden_drop_points[0][1])  # Drop Warden, bottom-right

    time.sleep(9)

    keyboard.send('a') # switch to Rage spell
    rage_drop_points = [
        (427, 267),
        (504, 219),
        (565, 168)
    ]
    random.shuffle(rage_drop_points)
    for point in rage_drop_points:
        do_click(point[0], point[1])

    time.sleep(5)
    rage_drop_points2 = [
        (393, 217),
        (481, 151)
    ]

    rage_chosen_coord = random.choice(rage_drop_points2)
    do_click(rage_chosen_coord[0], rage_chosen_coord[1])

    eagle_artillery_imgs = [
        (assets_path + '\\mv_assets\\eagle_lvl5.png', 'Eagle Artillery Level 5'),
        (assets_path + '\\mv_assets\\eagle_lvl4.png', 'Eagle Artillery Level 4'),
        # (assets_path + '\\mv_assets\\eagle_lvl3.png', 'Eagle Artillery Level 3'),
        # (assets_path + '\\mv_assets\\eagle_lvl2.png', 'Eagle Artillery Level 2'),
        # (assets_path + '\\mv_assets\\eagle_lvl1.png', 'Eagle Artillery Level 1')
    ]

    for img, level in eagle_artillery_imgs:
        location = check_image_presence(img)
        if location:
            setlog(f"{level} detected!", "info")
            x, y, _, _ = location
            window_rect = get_window_rect(window_title)
            relative_x = x - window_rect[0]
            relative_y = y - window_rect[1]
            do_click(relative_x, relative_y, 'Drop Freeze Spell on Eagle Artillery')
            break


    time.sleep(4)
    keyboard.send('r')
    do_click(220, 273, 'Drop Champion')

    champ_drop_points = [
        (116, 222),
        (667, 84),
        (605, 294),
        (325, 364),
    ]

    champ_chosen_coord = random.choice(champ_drop_points)
    do_click(champ_chosen_coord[0], champ_chosen_coord[1])

    # TODO - make freeze spell deployment random and make 3 drop points for Champion and randomize it and pick one

    setlog("Done deploying troops!", "success")

def play_sound():
    sound_path = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\sound\tokyo_drift.mp3'
    pygame.mixer.init()
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play()
    time.sleep(10)
    pygame.mixer.music.stop()
            # Loop until the music playback ends
    # while pygame.mixer.music.get_busy():
    #     # Allow the program to continue running
    #     pygame.time.Clock().tick(10)  # Adjust tick rate as needed
    pygame.mixer.quit()

def mv_return_home(assets_path):
    return_home_btn_img = assets_path + '\\test\\mv_return_home_btn.png'

    timeout = 120  # timeout in seconds
    start_time = time.time()
    setlog("Waiting for return home button to appear", "info")
    while not find_image_within_window(return_home_btn_img, confidence=0.7):
        if time.time() - start_time > timeout:
            setlog("Something went wrong on detecting return home button", "error")
            do_click(489, 474) # just click it
            break
        time.sleep(1)

    time.sleep(2)
    do_click(489, 474) # just click the return home button
    return True

def detect_loot(assets_path):
    next_btn_img = assets_path + '\\test\\next_btn.png'

    targets = {
        'gold': 400000,
        'elixir': 400000,
        # 'dark_elixir': 2000
    }

    while 1:
        time.sleep(3)
        if get_resources_value(resource_target='gold', target_val=400000) and get_resources_value(resource_target='elixir', target_val=400000): # or get_resources_value(resource_target='dark_elixir', target_val=2000):
            setlog("Found a base!", "success")
            return True
        else:
            try:
                click_next(assets_path)
                setlog("Searching for opponent...", "info")
                while not check_image_presence(next_btn_img, confidence=0.8):
                    time.sleep(0.2)
            except Exception as e:
                setlog(f"Error clicking next button: {e}", "error")
                return False

if __name__ == '__main__':

    # checkArmy(assets_path)
    # EdragLoons_strat()
    eagle_artillery_imgs = [
        (assets_path + '\\mv_assets\\buildings\\eagle_lvl5.png', 'Eagle Artillery Level 5'),
        (assets_path + '\\mv_assets\\buildings\\eagle_lvl4.png', 'Eagle Artillery Level 4')
        # (assets_path + '\\mv_assets\\buildings\\eagle_lvl3.png', 'Eagle Artillery Level 3'),
        # (assets_path + '\\mv_assets\\buildings\\eagle_lvl2.png', 'Eagle Artillery Level 2'),
        # (assets_path + '\\mv_assets\\buildings\\eagle_lvl1.png', 'Eagle Artillery Level 1')
    ]

    for img, level in eagle_artillery_imgs:
        location = check_image_presence(img, confidence=0.7)
        if location:
            setlog(f"{level} detected!", "info")
            x, y, _, _ = location
            window_rect = get_window_rect(window_title)
            relative_x = x - window_rect[0]
            relative_y = y - window_rect[1]
            do_click(relative_x, relative_y, 'Drop Freeze Spell on Eagle Artillery')
            break
        else:
            setlog(f"{level} not detected!", "warning")
            # break

    # monolith_img = assets_path + '\\mv_assets\\buildings\\monolith_lvl.png'
    # monolith_location = check_image_presence(monolith_img, confidence=0.7)
    # if monolith_location:
    #     x, y, _, _ = monolith_location
    #     window_rect = get_window_rect(window_title)
    #     relative_x = x - window_rect[0]
    #     relative_y = y - window_rect[1]
    #     do_click(relative_x, relative_y, 'Drop Freeze Spell on Monolith')
    # else:
    #     setlog("Monolith not detected!", "warning")
