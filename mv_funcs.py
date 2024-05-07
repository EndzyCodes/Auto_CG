
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

    click,
    click_drag,
    scroll_to_zoom,

    setlog
)
from cg_funcs import purge_challenge, pick_challenge

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
# from bb_funcs import bb_attack_loop

import time
import random
import pyautogui
import keyboard
import pygame


def is_army_btn_visible(click=False):

    img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\army_btn.png'

    count = 0
    while 1: 
        if not check_image_presence(img, confidence=0.8):
            time.sleep(0.3)
            count += 1
            if count == 1: setlog("Waiting for army tab to appear", "info")
        else:
            setlog("Army tab found", "success")
            click(867, 262)
            click(867, 262)
            click(867, 262)
            if click:
                if click_random_within_image(check_image_presence(img, confidence=0.8)):
                    time.sleep(1)
                    setlog("Clicked on army tab", "success")
                    return True
                else:
                    setlog("No army tab", "info")
                    return False
            return True

def check_daily_reward():
    img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\claim_btn.png'
    claim_btn_location = check_image_presence(img, confidence=0.9)
    if find_image(img, confidence=0.9):
        if click_random_within_image(claim_btn_location):
            time.sleep(1)
            click(867, 262) # click away
            setlog("Claimed daily reward", "success")
            return True
        else:
            setlog("No daily reward1", "info")
            return False
    else:
        setlog("No daily reward", "info")
        return False

def collect_resources():
    gold_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\gold.png'
    elixir_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\elixir.png'
    dark_elixir_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\dark_elixir.png'
    
    # Create a list of resource images
    resource_images = [gold_img, elixir_img, dark_elixir_img]
    
    # Randomize the order of resource collection
    random.shuffle(resource_images)

    collected_resources = False

    for resource_img in resource_images:
        resource_location = check_image_presence(resource_img, confidence=0.8)
        if find_image(resource_img):
            try:
                click_random_within_image(resource_location)
            except pyautogui.ImageNotFoundException:
                setlog(f"Image: {resource_img} not found", "info")
            resource_name = resource_img.split('\\')[-1].split('.')[0].capitalize()
            setlog(f"Collected {resource_name}", "info")
            collected_resources = True

    if collected_resources:
        setlog("Resources collected", "info")
    else:
        setlog("No resources collected", "info")

    return collected_resources

def main2(skip_acc_num=0): # for purging loop
    # when calling main function, put the acc number that you are currently playing coc manually, see the coc emulator switch acc to know what acc number to skip

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
        if find_image_within_window(r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\daily_reward.png'):
            setlog("Daily reward window found", "success")
            click(197, 250)
            click(341, 252)
            click(485, 252)
            click(203, 401)
            click(341, 404)
            click(483, 404)

        click(884, 242) # click away first just in case if there is a window pausinging the village
        scroll_to_zoom((716, 117), 10)
        # time.sleep(1)
        click_drag(716, 117, 419, 376)


        time.sleep(1)
        collect_resources()
        # click(252, 134) # click clan games


        time.sleep(3) # wait for clan games to open/load
        purge_challenge()
        time.sleep(1)

def get_resources_value(resource_target='', target_val=400000):
    # Define regions and image paths
    regions = {
        'gold': (46, 86, 70, 24),
        'elixir': (43, 108, 72, 24),
        'dark_elixir': (43, 131, 67, 24)
    }
    
    image_paths = {
        'gold': r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\test\gold_loot.png',
        'elixir': r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\test\elixir_loot.png',
        'dark_elixir': r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\test\dark_elixir_loot.png'
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
            print(f'{resource_target}: {value} - True')
            return True
        else:
            print(f'{resource_target}: {value} - False')
            return False
    else:
        print(f'{resource_target}: Error extracting value')
        return None

def click_next():
    next_btn_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\test\next_btn.png'

    if click_random_within_image(check_image_presence(next_btn_img, confidence=0.8)):
        print('Clicked next')
        return True
    else:
        setlog("No next button", "error")

def click_drag_troops(x, y, x_moveTo, y_moveTo, duration=0.175, debug=False):
    # use case: click_drag(716, 117, 419, 376)
    window_rect = get_window_rect(window_title)

    offset_x = window_rect[0] + random.randint(-3,5)
    offset_y = window_rect[1] + random.randint(-3,5)
    absolute_x = window_rect[0] + offset_x
    absolute_y = window_rect[1] + offset_y

    # absolute_x = window_rect[0] + x
    # absolute_y = window_rect[1] + y

    offset_x_moveTo = window_rect[0] + random.randint(-3,5)
    offset_y_moveTo = window_rect[1] + random.randint(-3,5)
    absolute_x_moveTo = window_rect[0] + x_moveTo + offset_x_moveTo
    absolute_y_moveTo = window_rect[1] + y_moveTo + offset_y_moveTo

    # absolute_x_moveTo = window_rect[0] + x_moveTo
    # absolute_y_moveTo = window_rect[1] + y_moveTo

    if debug: setlog(f"Moving from ({x}, {y}) to ({x_moveTo}, {y_moveTo})", "info")

    pyautogui.moveTo(absolute_x, absolute_y, duration=duration)
    # time.sleep(0.5)
    pyautogui.mouseDown()
    time.sleep(0.2)
    pyautogui.moveTo(absolute_x_moveTo, absolute_y_moveTo, duration=1.175)
    time.sleep(0.2)
    pyautogui.mouseUp()

def superBarbs_strat_deploy():
    scroll_to_zoom((300, 353), 10)
    click(164, 502) # click troop - super barb

    # Randomly decide deployment order (batch1_first = True means batch 1 deploys first)
    batch1_first = random.choice([True, False])

    if batch1_first:
        setlog("Deploying troops in batch 1 first", "info")
        # Batch 1 deploy
        click_drag(636, 314, 460, 200)  # Drag to bottom-right
        click_drag_troops(62, 185, 373, 417)
        click_drag_troops(440, 434, 767, 192)

        # Batch 2 deploy
        click_drag(467, 155, 456, 412)  # Drag to top side
        click_drag_troops(770, 314, 482, 102)
        click_drag_troops(409, 89, 96, 322)
    else:
        setlog("Deploying troops in batch 2 first", "info")
        # Batch 2 deploy
        click_drag(467, 155, 456, 412)  # Drag to top side
        click_drag_troops(770, 314, 482, 102)
        click_drag_troops(409, 89, 96, 322)

        # Batch 1 deploy
        click_drag(636, 314, 460, 200)  # Drag to bottom-right
        click_drag_troops(62, 185, 373, 417)
        click_drag_troops(440, 434, 767, 192)

    #  drop troops again in bottom just in case there is troops left
    click_drag(636, 314, 460, 200) # drag to bottom-right
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
            click(207, 68)  # Drop cc
        elif unit == 'King':
            keyboard.press('q'); time.sleep(1); keyboard.release('q')  # King
            click(222, 295)  # Drop King
        elif unit == 'Champion':
            keyboard.press('r'); time.sleep(0.5); keyboard.release('r')  # Champion
            click(220, 273)  # Drop Champion
        elif unit == 'Queen':
            keyboard.press('w'); time.sleep(0.5); keyboard.release('w')  # Queen
            click(711, 233)  # Drop Queen
        elif unit == 'Warden':
            keyboard.press('e'); time.sleep(0.5); keyboard.release('e')  # Warden
            click(703, 253)  # Drop Warden
    
    # Randomly activate hero abilities after a delay
    time.sleep(10)  # Wait for 10 seconds before activating abilities
    abilities_to_activate = random.sample(['King', 'Champion', 'Queen', 'Warden'], k=2)  # Randomly select 2 heroes to activate
    for ability in abilities_to_activate:
        if ability == 'King':
            keyboard.press('q'); time.sleep(0.5); keyboard.release('q')  # King ability
            click(296, 485)
        elif ability == 'Champion':
            keyboard.press('r'); time.sleep(0.5); keyboard.release('r')  # Champion ability
        elif ability == 'Queen':
            keyboard.press('w'); time.sleep(0.5); keyboard.release('w')  # Queen ability
        elif ability == 'Warden':
            keyboard.press('e'); time.sleep(0.5); keyboard.release('e')  # Warden ability

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

def mv_return_home():
    return_home_btn_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\test\mv_return_home_btn.png'

    timeout = 90  # timeout in seconds
    start_time = time.time()
    setlog("Waiting for return home button to appear", "info")
    while not find_image_within_window(return_home_btn_img, confidence=0.7):
        if time.time() - start_time > timeout:
            setlog("Something went wrong on detecting return home button", "error")
            break
        if click_random_within_image(check_image_presence(return_home_btn_img, confidence=0.7)):
            break
        time.sleep(1)

    return True

def main_village_attack_loop(isSwitchAcc=False):

    next_btn_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\test\next_btn.png'
    atk_btn_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\test\atk_btn.png'
    find_match_btn_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\test\find_match_btn.png'

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
                superBarbs_strat_deploy()
                mv_return_home()
                break
            else:
                try:
                    click_next()
                    setlog("Searching for opponent...", "info")
                    while not check_image_presence(next_btn_img, confidence=0.8):
                        time.sleep(0.2)
                except Exception as e:
                    setlog(f"Error clicking next button: {e}", "error")
                    break

        if is_army_btn_visible():
            click(867, 262) # click away for any window popup
            setlog("We are back in the main village!", "success")

        if is_army_btn_visible(click=True): # open army window
            click(674, 96) # click quick train
            time.sleep(1)
            click(733, 176) # click train, previous army
            click(867, 262) # click away

def is_army_full():

    troop_count_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\test\troop_count.png'

    # region = (1263, 697, 118, 30)
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
