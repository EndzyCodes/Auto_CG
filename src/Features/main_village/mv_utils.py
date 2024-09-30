import time, random, pyautogui, keyboard, pygame
from ...Functions.image_detection import (
    find_image_within_window,
    check_image_presence,
    click_random_within_image,
    find_image
)
from ...Functions.window_utils import (
    get_coc_window,
    get_window_rect,
    window_title
)
from ...Functions.click_utils import (
    do_click,
    click_drag,
    scroll_to_zoom
)
from ...Features.clan_games.cg_utils import purge_challenge
from ...Features.collect_resources.collect_res_main import collect_resources
from ...Features.attack.army_camp import is_army_btn_visible, isCampFull
from ...Functions.ocr_utils import extract_digit_from_image
from ...Functions.acc_switching_utils import switch_acc
from ...Functions.logging_utils import setlog
from ...config import assets_path

def check_daily_reward(assets_path):

    img = assets_path + '\\claim_btn.png'
    claim_btn_location = check_image_presence(img, confidence=0.9)
    if find_image(img, confidence=0.9):
        if click_random_within_image(claim_btn_location):
            time.sleep(1)
            do_click(867, 262) # click away
            setlog("Claimed daily reward", "success")
            return True
        else:
            setlog("No daily reward1", "info")
            return False
    else:
        setlog("No daily reward", "info")
        return False

def main2(skip_acc_num=0): # for purging loop
    # when calling main function, put the acc number that you are currently playing coc manually, see the coc emulator switch acc to know what acc number to skip
    global assets_path

    count = 0
    while 1:
        # window_rect=get_window_rect(window_title)
        get_coc_window(window_title)
        count += 1
        if count > 21: #or count == 22:
            count = 1 # reset count to 1 so it can start counting again from 1

        if count == skip_acc_num:
            # if skip_acc_num is same with the value on count then increment again so it can skip the account number
            setlog(f"Skipping account number {count}", "info")
            count += 1
            # continue
        switch_acc(count)

        is_army_btn_visible() # if army btn is visible then it means the account has loaded

        # check_daily_reward() # this for accounts that have been opened just now, "Chief you're back!"

        # click all possible claims button
        if find_image_within_window(assets_path + '\\daily_reward.png'):
            setlog("Daily reward window found", "success")
            do_click(197, 250)
            do_click(341, 252)
            do_click(485, 252)
            do_click(203, 401)
            do_click(341, 404)
            do_click(483, 404)

        do_click(884, 242) # click away first just in case if there is a window pausinging the village
        scroll_to_zoom((716, 117), 10)
        # time.sleep(1)
        click_drag(716, 117, 419, 376)


        time.sleep(1)
        collect_resources()
        # do_click(252, 134) # click clan games


        time.sleep(3) # wait for clan games to open/load
        purge_challenge()
        time.sleep(1)

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

def click_next(assets_path):
    next_btn_img = assets_path + '\\test\\next_btn.png'

    if click_random_within_image(check_image_presence(next_btn_img, confidence=0.8)):
        print('Clicked next')
        return True
    else:
        setlog("No next button", "error")

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
def superBarbs_strat():
    scroll_to_zoom((300, 353), 10)
    do_click(164, 502) # click troop - super barb
    # time.sleep(2)
    # Randomly decide deployment order (batch1_first = True means batch 1 deploys first)
    batch1_first = random.choice([True, False])

    if batch1_first:
        setlog("Deploying troops in batch 1 first", "info")
        # Batch 1 deploy
        click_drag(636, 314, 460, 200)  # Drag to bottom-right
        # time.sleep(1)
        click_drag_troops(62, 185, 373, 417)
        click_drag_troops(440, 434, 767, 192)

        # Batch 2 deploy
        click_drag(467, 155, 456, 412)  # Drag to top side
        # time.sleep(1)
        click_drag_troops(770, 314, 482, 102)
        click_drag_troops(409, 89, 96, 322)
    else:
        setlog("Deploying troops in batch 2 first", "info")
        # Batch 2 deploy
        click_drag(467, 155, 456, 412)  # Drag to top side
        # time.sleep(1)
        click_drag_troops(770, 314, 482, 102)
        click_drag_troops(409, 89, 96, 322)

        # Batch 1 deploy
        click_drag(636, 314, 460, 200)  # Drag to bottom-right
        # time.sleep(1)
        click_drag_troops(62, 185, 373, 417)
        click_drag_troops(440, 434, 767, 192)

    #  drop troops again in bottom just in case there is troops left
    click_drag(636, 314, 460, 200) # drag to bottom-right
    # time.sleep(1)
    click_drag_troops(62, 185, 373, 417)
    click_drag_troops(440, 434, 767, 192)

    # Randomize deployment order
    deployment_order = ['cc', 'King', 'Champion', 'Queen', 'Warden']
    random.shuffle(deployment_order)

    setlog("Deploying heroes in randomized order", "info")
    setlog(f"Deployment order: {deployment_order}", "info")
    # Drop clan castle troops (cc) and heroes according to the randomized order
    for unit in deployment_order:
        if unit == 'cc':
            keyboard.press('z'); time.sleep(0.5); keyboard.release('z')  # Clan castle
            do_click(207, 68)  # Drop cc
        elif unit == 'King':
            keyboard.press('q'); time.sleep(1); keyboard.release('q')  # King
            do_click(222, 295)  # Drop King
        elif unit == 'Champion':
            keyboard.press('r'); time.sleep(0.5); keyboard.release('r')  # Champion
            do_click(220, 273)  # Drop Champion
        elif unit == 'Queen':
            keyboard.press('w'); time.sleep(0.5); keyboard.release('w')  # Queen
            do_click(711, 233)  # Drop Queen
        elif unit == 'Warden':
            keyboard.press('e'); time.sleep(0.5); keyboard.release('e')  # Warden
            do_click(703, 253)  # Drop Warden

    # Randomly activate hero abilities after a delay
    time.sleep(10)  # Wait for 10 seconds before activating abilities
    abilities_to_activate = random.sample(['King', 'Champion', 'Queen', 'Warden'], k=2)  # Randomly select 2 heroes to activate
    for ability in abilities_to_activate:
        if ability == 'King':
            keyboard.press('q'); time.sleep(0.5); keyboard.release('q')  # King ability
            do_click(296, 485)
        elif ability == 'Champion':
            keyboard.press('r'); time.sleep(0.5); keyboard.release('r')  # Champion ability
        elif ability == 'Queen':
            keyboard.press('w'); time.sleep(0.5); keyboard.release('w')  # Queen ability
        elif ability == 'Warden':
            keyboard.press('e'); time.sleep(0.5); keyboard.release('e')  # Warden ability

    setlog("Done deploying troops!", "success")

def EdragLoons_strat():
    # TH14 - 300 army camps space | 8 Edrags 12 Loons | 4 rage 3 Freeze | CC Edrag loons, 2 lightning 1 Freeze
    # TH13 - Same as TH14
    # TH12 - 280 army camps space | 8 Edrags 8 Loons | 4 rage 3 Freeze | CC Edrag loons, 2 lightning
    # TH11 - 260 army camps space | 8 Edrags 4 Loons | same as TH12 | same as TH12

    global assets_path
    scroll_to_zoom((300, 353), 10)

    #* ---- BOTTOM-RIGHT DEPLOYMENT ----
    click_drag(636, 314, 460, 200) # Drag to bottom-right
    king_icn_img = assets_path + '\\donate_assets\\king_icon.png'
    queen_icn_img = assets_path + '\\donate_assets\\queen_icon.png'

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

    keyboard.send('r')
    do_click(220, 273, 'Drop Champion')

    # TODO - make freeze spell deployment random and make 3 drop points for Champion and randomize it and pick one

    setlog("Done deploying troops!", "success")

#* ---- END OF ATTACK STRATEGIES ----

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

def main_village_attack_loop(isSwitchAcc=False):
    global assets_path

    next_btn_img = assets_path + '\\test\\next_btn.png'
    atk_btn_img = assets_path + '\\test\\atk_btn.png'
    find_match_btn_img = assets_path + '\\test\\find_match_btn.png'

    # Define resource targets and their corresponding target values
    targets = {
        'gold': 400000,
        'elixir': 400000,
        # 'dark_elixir': 2000
    }

    atk_count = 0
    count = 1

    while 1:

        atk_count += 1
        setlog(f"Attack round {atk_count}", "info")
        if isSwitchAcc and atk_count > 2:
            count += 1
            setlog("Attack round limit reached", "info")
            setlog("Switching account...", "info")
            switch_acc(count)
            atk_count = 0 # reset attack count
            if is_army_btn_visible():
                continue
        else:
            setlog("Account switching not enabled", "info")
            setlog("Staying on current account", "info")
            atk_count = 0 # reset attack count

        while not check_image_presence(atk_btn_img, confidence=0.8):
            time.sleep(0.2)
        click_random_within_image(check_image_presence(atk_btn_img, confidence=0.8))

        while not check_image_presence(find_match_btn_img, confidence=0.8):
            time.sleep(0.2)
        click_random_within_image(check_image_presence(find_match_btn_img, confidence=0.8))

        setlog("Searching for opponent...", "info")
        while not check_image_presence(next_btn_img, confidence=0.8):
            time.sleep(0.2)

        while 1:
            time.sleep(3)
            # Check each resource target and take action if a base is found
            # if any(get_resources_value(resource_target=resource, target_val=value) for resource, value in targets.items()):
            if get_resources_value(resource_target='gold', target_val=300000) and get_resources_value(resource_target='elixir', target_val=300000): # or get_resources_value(resource_target='dark_elixir', target_val=2000):
                setlog("Found a base!", "success")
                play_sound()
                superBarbs_strat()
                mv_return_home(assets_path)
                break
            else:
                try:
                    click_next(assets_path)
                    setlog("Searching for opponent...", "info")
                    while not check_image_presence(next_btn_img, confidence=0.8):
                        time.sleep(0.2)
                except Exception as e:
                    setlog(f"Error clicking next button: {e}", "error")
                    break

        if is_army_btn_visible():
            do_click(867, 262) # click away for any window popup
            setlog("We are back in the main village!", "success")

        if is_army_btn_visible(click=True): # open army window
            do_click(674, 96) # click quick train
            time.sleep(1)
            do_click(733, 176) # click train, previous army
            do_click(867, 262) # click away

        keyboard.press('1'); keyboard.release('1')

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

def atk_loop(assets_path):

    next_btn_img = assets_path + '\\test\\next_btn.png'
    atk_btn_img = assets_path + '\\test\\atk_btn.png'
    find_match_btn_img = assets_path + '\\test\\find_match_btn.png'

    atk_count = 0
    while 1:
        checkArmy(assets_path)
        atk_count += 1
        setlog(f"Attack round {atk_count}", "info")
        # while not (atk_btn_loc := check_image_presence(atk_btn_img, confidence=0.7)):
        #     time.sleep(0.2)
        # click_random_within_image(atk_btn_loc)

        do_click(59, 502) # click attack button
        while not (match_btn_loc := check_image_presence(find_match_btn_img, confidence=0.7)):
            time.sleep(0.2)
        click_random_within_image(match_btn_loc)

        setlog("Searching for opponent...", "info")
        while not check_image_presence(next_btn_img, confidence=0.8):
            time.sleep(0.2)

        if detect_loot(assets_path):
            play_sound()
            superBarbs_strat()
            mv_return_home(assets_path)

        while not is_army_btn_visible(assets_path):
            time.sleep(0.2)
        do_click(867, 262) # click away for any window popup
        setlog("We are back in the main village!", "success")

        if is_army_btn_visible(assets_path, click=True): # open army window
            do_click(674, 96, random_click=False) # click quick train
            time.sleep(1)
            do_click(733, 176, random_click=False) # click train, previous army
            do_click(867, 262) # click away
        setlog(f"Attack round {atk_count}", "info")
import os
def dmg_percentage_change(assets_path):

    window_rect = get_window_rect(window_title)

    dmg_percentage_img = assets_path + '\\mv_assets\\damage_percentage.png'
    region_ss = (window_rect[0] + 791, window_rect[1] + 401, 137, 63)

    # time.sleep(2)

    # setlog(f"Damage percentage: {percentage}", "info")

    while 1:
        time.sleep(1)
        ss = pyautogui.screenshot(region=region_ss)
        ss.save(dmg_percentage_img)

        percentage = extract_digit_from_image(dmg_percentage_img)
        if percentage is not None and percentage != 100:
            percentage = int(str(percentage)[:2])
        previous_percentage = percentage
        start_time = time.time()
        if percentage is not None:
        #     if percentage > 33:
        #         setlog("True", "info")
        #         setlog(f"Damage percentage: {percentage}", "info")
        #     else:
        #         setlog("False", "info")
        #         setlog(f"Damage percentage: {percentage}", "info")
        # else:
        #     setlog("Failed to extract damage percentage", "error")

            if time.time() - start_time > 5:
                if percentage == previous_percentage:
                    setlog("Damage percentage did not change within 10 seconds", "warning")
                break
            previous_percentage = percentage
            time.sleep(1)
            percentage = extract_digit_from_image(dmg_percentage_img)

        os.remove(dmg_percentage_img)

if __name__ == '__main__':

    dmg_percentage_change(assets_path)
