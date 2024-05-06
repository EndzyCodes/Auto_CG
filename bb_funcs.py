
from Functions import (
    get_coc_window,

    click_random_within_image,
    check_image_presence,
    find_image_within_window,

    click,
    click_drag,
    scroll_to_zoom,

    setlog,
    switch_acc
)
# from mv_funcs import is_army_btn_visible
import time
# import random
# import pyautogui
# import keyboard
# import pygame

def deploy_troops(sec_vill_battle=False):

    if sec_vill_battle:
        setlog("Deploying troops on the 2nd village battle ground", "info")
        setlog("Dropping loons", "info")
        click(160, 487) # click hero
        click(583, 316) # drop hero
        time.sleep(10)

        click(589, 485) # click loon icon just to be sure
        # drop loons
        click(515, 349)
        # click(591, 314)
        click(630, 279)
        # click(678, 243)
        click(740, 200)
        click(591, 314)
        click(678, 243)

        time.sleep(3) # wait a bit before dropping minions
        setlog("Dropping minions", "info")
        # click all possible  minions icon
        click(417, 507)
        click(480, 506)
        click(532, 513)
        # minions drop points
        for i in range(3):
            click(515, 349)
            click(591, 314)
            click(630, 279)
            click(678, 243)
            click(740, 200)

        time.sleep(12)
        setlog("Activating hero ability", "info")
        click(165, 509) # activate hero ability
    else:
        setlog("Deploying troops on the 1st village battle ground", "info")
        setlog("Deploying", "info")
        click(160, 487) # click hero
        click(583, 316) # drop hero

        time.sleep(10) # wait a bit before dropping balloons
        setlog("Dropping loons", "info")
        click(231, 505) # click balloon icon

        # ballons drop points
        click(521, 375) 
        # click(579, 333)
        click(630, 279)
        # click(619, 303)
        click(740, 200)

        time.sleep(3) # wait a bit before dropping minions
        setlog("Dropping minions", "info")
        click(417, 507) # click minions icon

        # minions drop points
        for i in range(3):
            click(515, 349)
            click(591, 314)
            click(630, 279)
            click(678, 243)
            click(740, 200)

        time.sleep(10)
        setlog("Activating hero ability", "info")
        click(165, 509) # activate hero ability

def boost_troop_heroes():
    click(39, 432) # click army tab
    
    click(473, 302) # click hero boost button
    click(473, 352) # click to confirm boost
    
    time.sleep(1)
    
    click(596, 308) # click troop boost button
    click(596, 358) # click to confirm boost
    
    click(902, 284) # click away

def bb_return_home():
    return_home_btn_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\bb_assets\return_home_btn.png'
    hero_ability_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\bb_assets\hero_ability.png'

    timeout = 90  # timeout in seconds
    start_time = time.time()
    setlog("Waiting for return home button to appear", "info")
    while not find_image_within_window(return_home_btn_img):
        if time.time() - start_time > timeout:
            setlog("Something went wrong on detecting return home button", "error")
            break
        time.sleep(1)
        if find_image_within_window(hero_ability_img, confidence=0.9):
            if click_random_within_image(check_image_presence(hero_ability_img, confidence=0.9)):
                setlog("Hero ability is ready again, clicking it now", "info")

    # if find_image_within_window(return_home_btn_img):
    if click_random_within_image(check_image_presence(return_home_btn_img, confidence=0.8)):
        setlog("Clicked return home button", "success")
        return True
    else:
        setlog("Failed to click return home button", "error")
        return False
    # else:
    #     setlog("Return home button did not appear", "warning")

def bb_attack_time_limit():
    import keyboard
    count = 1
    start_time = time.time()
    while True:
        # main(attack_only_no_cg=True, enable_gem_cooldown=False, clan_games_mode=False)
        bb_attack_loop()
        # if time.time() - start_time >= 90 * 60:  # 90 minutes in seconds
        if time.time() - start_time >= 60 * 60:  # 2 hours in seconds
            keyboard.press_and_release('esc')
            time.sleep(1)
            click(534, 349)
            break
            # count += 1
            # if count > 21:
            #     count = 1
            #     switch_acc(count)
            #     is_army_btn_visible()
            # else:
            #     setlog("time limit reached, switching account...", "info")
            #     switch_acc(count)
            #     is_army_btn_visible()
    return True

found_opponent = False
def attack_BB():
    get_coc_window("Clash of Clans")
    global found_opponent

    bb_atk_btn_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\bb_assets\bb_atk_btn.png'
    if find_image_within_window(bb_atk_btn_img):
        if click_random_within_image(check_image_presence(bb_atk_btn_img, confidence=0.8)):
            setlog("Clicked attack button", "success")
            time.sleep(1.5)
        else:
            setlog("Failed to attack button", "error")
    else:
        setlog("Builder base attack button not found", "error")

    find_now_btn_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\bb_assets\find_now_btn.png'
    if click_random_within_image(check_image_presence(find_now_btn_img, confidence=0.8)):
        setlog("Clicked find now button", "success")
        time.sleep(1.5)
    else:
        setlog("Failed to click find now button", "error")

    cancel_btn_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\bb_assets\cancel_btn.png'
    if find_image_within_window(cancel_btn_img):
        time.sleep(0.5)
        setlog("Finding an opponent...", "info")
        while find_image_within_window(cancel_btn_img):
            time.sleep(0.5)
        else:
            setlog("Found an opponent", "success")
            found_opponent = True

    time.sleep(3) # wait a bit to load battle ground
    scroll_to_zoom((300, 353), 10)
    time.sleep(1)
    click_drag(743, 429, 414, 200)
    time.sleep(1)
    deploy_troops()

    return_home_btn_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\bb_assets\return_home_btn.png'
    sec_vill_loon = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\bb_assets\sec_vill_loon.png'
    hero_ability_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\bb_assets\hero_ability.png'

    timeout = 120  # timeout in seconds
    start_time = time.time()
    setlog("Waiting for battle to finish", "info")
    while not find_image_within_window(return_home_btn_img):
        if time.time() - start_time > timeout:
            break
        time.sleep(1)
        if find_image_within_window(hero_ability_img, confidence=0.9):
            if click_random_within_image(check_image_presence(hero_ability_img, confidence=0.9)):
                setlog("Hero ability is ready again, clicking it now", "info")
        if find_image_within_window(sec_vill_loon):
            # setlog("We are at the 2nd village battle ground", "info")
            break
        if find_image_within_window(hero_ability_img, confidence=0.9):
            if click_random_within_image(check_image_presence(hero_ability_img, confidence=0.9)):
                setlog("Hero ability is ready again, clicking it now", "info")

    if find_image_within_window(return_home_btn_img):
        if click_random_within_image(check_image_presence(return_home_btn_img, confidence=0.8)):
            setlog("Clicked return home button", "success")
        else:
            setlog("Failed to click return home button", "error")
    else:
        # setlog("Return home button did not appear", "warning")
        # setlog("Maybe we are on the next village")
        time.sleep(1)
        # balloon_troop = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\bb_assets\balloon_troop.png'
        if find_image_within_window(sec_vill_loon):
            setlog("We are at the 2nd village battle ground", "info")
            # if click_random_within_image(check_image_presence(sec_vill_loon, confidence=0.9)):
            #     setlog("Clicked balloon troop", "success")
            # else:
            #     setlog("Failed to click balloon troop", "error")

            # setlog("Maybe we are on the next village", "info")
            time.sleep(3) # wait a bit to load battle ground
            scroll_to_zoom((300, 353), 10)
            time.sleep(1)
            click_drag(743, 429, 414, 200)
            time.sleep(1)
            deploy_troops(sec_vill_battle=True) # deploy troops on the 2nd village battle ground
            found_opponent = False
            bb_return_home()

def go_to_bb(go_back_main=False):

    boat_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\bb_assets\boat.png'

    if go_back_main:
        scroll_to_zoom((716, 117), 10)
        click_drag(854, 271, 700, 429)
        time.sleep(2)
        setlog("Going back to main village", "info")
        if find_image_within_window(boat_img, confidence=0.7):
            setlog("Found builder base boat", "success")
            if click_random_within_image(check_image_presence(boat_img, confidence=0.7)):
                setlog("Clicked builder base boat", "success")
                scroll_to_zoom((716, 117), 10)
                return True
            else:
                setlog("Failed to click builder base", "error")
                return False
    
    else:
        click_drag(470, 316, 725, 82)
        time.sleep(1)

        if find_image_within_window(boat_img):
            setlog("Found builder base boat", "success")
            if click_random_within_image(check_image_presence(boat_img, confidence=0.9)):
                setlog("Clicked builder base boat", "success")
                return True
            else:
                setlog("Failed to click builder base", "error")
                return False

def bb_attack_loop(isSwitchAcc=False):

    close_btn_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\close_btn.png'
    bb_atk_btn_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\bb_assets\bb_atk_btn.png'
    # challenge_completed_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\bb_assets\challenge_completed.png'

    cart_w_elixir = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\bb_assets\cart_with_elixir.png'
    btn_collect_elixir_cart = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\bb_assets\collect_elixir_cart.png'
    cart_full_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\bb_assets\elixir_cart_full.png'
    cart2_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\bb_assets\elixir_cart2.png'

    # if attack_only_no_cg:
    #TODO - detect if storage is full, put time limit per acc
    # if time limit reach it can close the game for 20 minute or it can switch account
    #TODO - implement:
    # if isSwitchAcc and isStoragesFull or time_limit_reached:
    #     setlog("Switching account...", "info")
    #     switch_account(count)
    #     continue
    start_time = time.time()
    while 1:
        time_left = int((60 * 60 - (time.time() - start_time)) / 60)
        setlog(f"Time left: {time_left} minutes", 'info')
        attack_BB()
        time.sleep(1)
        for i in range(20):
            time.sleep(0.5)
            if find_image_within_window(bb_atk_btn_img):
                setlog("We are back at builder base!", "success")
                time.sleep(2)
                click(867, 262) # click away just in case there is star bonus window
                click(867, 262)
                break
        #* Check cart for elixir then collect it
        scroll_to_zoom((716, 117), 10)
        click_drag(854, 271, 700, 429)
        setlog("Checking cart for elixir...", "info")
        time.sleep(3)
        if click_random_within_image(check_image_presence(cart_full_img, confidence=0.7)) or click_random_within_image(check_image_presence(cart2_img, confidence=0.7)):
            while not find_image_within_window(btn_collect_elixir_cart, confidence=0.7):
                time.sleep(0.2)
            if click_random_within_image(check_image_presence(btn_collect_elixir_cart, confidence=0.7)):
                setlog("Collected elixir cart", "success")
                time.sleep(1)
                click(867, 262) # click away
                click(867, 262)
            else:
                setlog("Failed to collect elixir cart, something wrong with collect_elixir_cart", "error")
        else:
            setlog("Cart does not have elixir yet", "info")
