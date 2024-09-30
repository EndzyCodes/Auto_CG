import time
import random
import keyboard
from ...Functions.image_detection import (
    find_image_within_window,
    click_random_within_image,
    check_image_presence
)
from ...Functions.click_utils import (
    do_click,
    click_drag,
    scroll_to_zoom
)
from ...Functions.logging_utils import setlog
from ...config import assets_path

def BB_is_army_btn_visible(click=False):

    img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\army_btn.png'

    count = 0
    while 1:
        if not check_image_presence(img, confidence=0.8):
            time.sleep(0.3)
            count += 1
            if count == 1: setlog("Waiting for army tab to appear", "info")
        else:
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

def deploy_troops(sec_vill_battle=False, is_2_camps=False):
    print(f'deploy_troops, is_2_camps: {is_2_camps}')

    if sec_vill_battle:
        setlog("Deploying troops on the 2nd village battle ground", "info")
        setlog("Deploying Hero", "info")
        do_click(157, 485, random_click=False) # click hero
        # do_click(583, 316) # drop hero
        click_points = [
            (515, 349),
            (630, 279),
            (740, 200),
            (591, 314),
            (678, 243)
        ]
        random_click_point = random.choice(click_points)
        do_click(random_click_point[0], random_click_point[1])

        time.sleep(10)

        do_click(589, 485) # click loon icon just to be sure
        #* ballons drop points
        #  randomize drop order
        click_points = [
            (521, 375),
            (630, 279),
            (740, 200)
        ]
        random.shuffle(click_points)
        for i, point in enumerate(click_points):
            # setlog(f"Iteration {i+1}: Dropping loon at {point}", "info")
            do_click(point[0], point[1])

        time.sleep(3) # wait a bit before dropping minions
        setlog("Dropping minions", "info")

        # if is_2_camps:
        #     setlog("Clicking minion from 2nd camp", "info")
        #     do_click(640, 490) # click minion on 2nd camp if the account has a 2nd camp
        # else:
            # click all possible  minions icon
        do_click(417, 507)
        do_click(480, 506)
        do_click(532, 513)
        #* minions drop points
        # randomize minion drop order
        minions = [(515, 349), (591, 314), (630, 279), (678, 243), (740, 200)]
        random.shuffle(minions)
        for _ in range(3):
            for point in minions:
                do_click(point[0], point[1])

        time.sleep(12)
        setlog("Activating hero ability", "info")
        do_click(165, 509) # activate hero ability
    else:
        setlog("Deploying troops on the 1st village battle ground", "info")
        setlog("Deploying Hero", "info")
        do_click(157, 485, random_click=False) # click hero
        # do_click(583, 316) # drop hero
        # randomize hero drop
        click_points = [
            (515, 349),
            (630, 279),
            (740, 200),
            (591, 314),
            (678, 243)
        ]
        random_click_point = random.choice(click_points)
        do_click(random_click_point[0], random_click_point[1])
        time.sleep(10) # wait a bit before dropping balloons

        setlog("Dropping loons", "info")
        do_click(231, 505) # click balloon icon

        #* ballons drop points
        #  randomize drop order
        click_points = [
            (521, 375),
            (630, 279),
            (740, 200)
        ]
        random.shuffle(click_points)
        for i, point in enumerate(click_points):
            # setlog(f"Iteration {i+1}: Dropping loon at {point}", "info")
            do_click(point[0], point[1])

        time.sleep(3) # wait a bit before dropping minions
        setlog("Dropping minions", "info")
        do_click(417, 507) # click minions icon

        #* minions drop points
        # randomize minion drop order
        minions = [(515, 349), (591, 314), (630, 279), (678, 243), (740, 200)]
        random.shuffle(minions)
        for _ in range(3):
            for point in minions:
                do_click(point[0], point[1])

        time.sleep(10)
        setlog("Activating hero ability", "info")
        do_click(165, 509) # activate hero ability

def boost_troop_heroes():
    do_click(39, 432) # click army tab

    do_click(473, 302) # click hero boost button
    do_click(473, 352) # click to confirm boost

    time.sleep(1)

    do_click(596, 308) # click troop boost button
    do_click(596, 358) # click to confirm boost

    do_click(902, 284) # click away

def bb_return_home():
    global assets_path

    return_home_btn_img = assets_path + '\\bb_assets\\return_home_btn2.png'
    hero_ability_img = assets_path + '\\bb_assets\\hero_ability2.png'
    connection_err_img = assets_path + '\\connection_error.png'

    timeout = 90  # timeout in seconds
    start_time = time.time()
    setlog("Waiting for return home button to appear", "info")
    while not find_image_within_window(return_home_btn_img):
        if time.time() - start_time > timeout:
            setlog("Something went wrong on detecting return home button", "error")
            break
        time.sleep(1)
        if (hero_ability_location := check_image_presence(hero_ability_img, confidence=0.9)):
            if click_random_within_image(hero_ability_location):
                setlog("Hero ability is ready again, clicking it now", "info")
        #* check for connection error
        if click_random_within_image(check_image_presence(connection_err_img)):
            setlog("Connection error detected, reconnecting...", "warning")
            if BB_is_army_btn_visible():
                return True

    # if find_image_within_window(return_home_btn_img):
    if click_random_within_image(check_image_presence(return_home_btn_img, confidence=0.8)):
        setlog("Clicked return home button", "success")
        return True
    else:
        setlog("Failed to click return home button", "error")
        return False
    # else:
    #     setlog("Return home button did not appear", "warning")

def go_to_bb(go_back_main=False):
    global assets_path

    boat_img = assets_path + '\\bb_assets\\boat.png'

    if go_back_main:
        scroll_to_zoom((716, 117), 10)
        click_drag(854, 271, 700, 429)
        time.sleep(3)
        setlog("Going back to main village", "info")
        if (boat_location := check_image_presence(boat_img, confidence=0.7)):
            if click_random_within_image(boat_location):
                setlog("Clicked builder base boat", "success")
                time.sleep(5)
                if BB_is_army_btn_visible():
                    scroll_to_zoom((716, 117), 10)
                    return True
                else:
                    setlog("Failed to click builder base", "error")
                    return False
            else:
                setlog("Failed to go back to main village, cannot find the boat", "error")
                return False

    else:
        scroll_to_zoom((716, 117), 10)
        click_drag(470, 316, 725, 82)
        time.sleep(2)

        if (boat_location := check_image_presence(boat_img, confidence=0.7)):
            if click_random_within_image(boat_location):
                setlog("Clicked builder base boat", "success")
                time.sleep(5)
                if BB_is_army_btn_visible():
                    return True
                else:
                    setlog("Failed to go to bb", "error")
                    return False
            else:
                setlog("Failed to click builder base boat", "error")
                return False

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
            do_click(534, 349)
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
def attack_BB(is_2_camps=False):

    global found_opponent
    global assets_path

    bb_atk_btn_img = assets_path + '\\bb_assets\\bb_atk_btn.png'
    if find_image_within_window(bb_atk_btn_img, confidence=0.7):
        if click_random_within_image(check_image_presence(bb_atk_btn_img, confidence=0.8)):
            setlog("Clicked attack button", "success")
            time.sleep(1.5)
        else:
            setlog("Failed to attack button", "error")
    else:
        setlog("Builder base attack button not found", "error")

    connection_err_img = assets_path + '\\connection_error.png'
    find_now_btn_img = assets_path + '\\bb_assets\\find_now_btn.png'
    while 1:
        while not click_random_within_image(check_image_presence(find_now_btn_img, confidence=0.8)):
            time.sleep(0.1)
            if click_random_within_image(check_image_presence(connection_err_img)):
                setlog("Connection error detected, reconnecting...", "warning")
                if BB_is_army_btn_visible():
                    continue # go back to loop
        else:
            setlog("Clicked find now button", "success")
            break

    cancel_btn_img = assets_path + '\\bb_assets\\cancel_btn.png'
    if find_image_within_window(cancel_btn_img):
        time.sleep(0.5)
        setlog("Finding an opponent...", "info")
        while find_image_within_window(cancel_btn_img):
            time.sleep(0.5)
        else:
            setlog("Found an opponent", "success")
            found_opponent = True


    troop_icn_img = assets_path + '\\bb_assets\\troop_icn.png'
    # if troop icon is visible it means the battle ground is loaded
    while not find_image_within_window(troop_icn_img):
        time.sleep(1)
    setlog("Battle ground loaded", "success")
    # time.sleep(3) # wait a bit to load battle ground
    scroll_to_zoom((300, 353), 10)
    time.sleep(1)
    click_drag(743, 429, 414, 200)
    time.sleep(1)
    deploy_troops(is_2_camps=is_2_camps)

    return_home_btn_img = assets_path + '\\bb_assets\\return_home_btn2.png'
    sec_vill_loon = assets_path + '\\bb_assets\\sec_vill_loon.png'
    hero_ability_img = assets_path + '\\bb_assets\\hero_ability2.png'
    connection_err_img = assets_path + '\\connection_error.png'

    timeout = 120  # timeout in seconds
    start_time = time.time()
    setlog("Waiting for battle to finish", "info")
    while not find_image_within_window(return_home_btn_img, confidence=0.7):
        if time.time() - start_time > timeout:
            break
        # time.sleep(1)
        if (hero_ability_location := check_image_presence(hero_ability_img, confidence=0.9)):
            if click_random_within_image(hero_ability_location):
                setlog("Hero ability is ready again, clicking it now", "info")
        if find_image_within_window(sec_vill_loon):
            # setlog("We are at the 2nd village battle ground", "info")
            break
        if (hero_ability_location := check_image_presence(hero_ability_img, confidence=0.9)):
            if click_random_within_image(hero_ability_location):
                setlog("Hero ability is ready again, clicking it now", "info")
        # check for connection error
        if click_random_within_image(check_image_presence(connection_err_img)):
            setlog("Connection error detected, reconnecting...", "warning")
            if BB_is_army_btn_visible():
                return True

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
            deploy_troops(sec_vill_battle=True, is_2_camps=is_2_camps) # deploy troops on the 2nd village battle ground
            found_opponent = False
            bb_return_home()

def bb_attack_loop(isSwitchAcc=False, is_2_camps=False):
    global assets_path

    close_btn_img = assets_path + '\\close_btn.png'
    bb_atk_btn_img = assets_path + '\\bb_assets\\bb_atk_btn.png'
    # challenge_completed_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\bb_assets\challenge_completed.png'

    cart_w_elixir = assets_path + '\\bb_assets\\cart_with_elixir.png'
    btn_collect_elixir_cart = assets_path + '\\bb_assets\\collect_elixir_cart.png'
    cart_full_img = assets_path + '\\bb_assets\\elixir_cart_full.png'
    cart2_img = assets_path + '\\bb_assets\\elixir_cart2.png'

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
        time_left = int((180 * 60 - (time.time() - start_time)) / 60)
        setlog(f"Time left: {time_left} minutes", 'info')
        attack_BB(is_2_camps=is_2_camps)
        time.sleep(1)
        for i in range(20):
            time.sleep(0.5)
            if find_image_within_window(bb_atk_btn_img):
                setlog("We are back at builder base!", "success")
                time.sleep(2)
                do_click(867, 262) # click away just in case there is star bonus window
                do_click(867, 262)
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
                do_click(867, 262) # click away
                do_click(867, 262)
            else:
                setlog("Failed to collect elixir cart, something wrong with collect_elixir_cart", "error")
        else:
            setlog("Cart does not have elixir yet", "info")

        if time.time() - start_time >= 180 * 60:  # 3 hours in seconds
            keyboard.press_and_release('esc')
            time.sleep(1)
            do_click(534, 349)
            break

if __name__ == '__main__':
    bb_attack_loop() # for attacking in bb endless (no clan games)
    # bb_attack_time_limit() # for attacking in bb with time limit (no clan games)
