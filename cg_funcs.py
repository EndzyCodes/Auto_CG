
from Functions import (
    click_random_within_image,
    check_image_presence,
    find_image_within_window,
    find_image,
    find_image_in_directory,
    find_multiple_images_in_directory,
    switch_acc,

    do_click,
    click_drag,
    scroll_to_zoom,

    setlog
)
from bb_funcs import attack_BB, go_to_bb
# from mv_funcs import is_army_btn_visible
import time

assets_path = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets'

def is_army_btn_visible(click=False):
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

def purge_challenge(gem_cooldown=False, purge_once=False):
    global assets_path

    ok_btn_img = assets_path + '\\okay_btn.png'
    gem_cd_img = assets_path + '\\gem_cd.png'

    purged = False
    start_btn_img = assets_path + '\\start_btn.png'
    trash_btn_img = assets_path + '\\trash_btn.png'
    home_vill_challenge_img = assets_path + '\\home_vill_challenge.png'
    running_challenge_img = assets_path + '\\running_challenge.png'
    challenge_cooldown_img = assets_path + '\\challenge_cooldown.png'
    # bb_vill_challenge_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\bb_vill_challenge.png'

    while 1:
        if find_image_within_window(challenge_cooldown_img, confidence=0.7):
            setlog("Purge is on cooldown", "info")
            time.sleep(1)
            do_click(867, 262) # click away to close clan games window
            do_click(867, 262) # click away just to be sure
            return True
        if find_image_within_window(home_vill_challenge_img):
            setlog("Home Village Challenge found", "success")

            click_random_within_image(check_image_presence(home_vill_challenge_img, confidence=0.8))
            time.sleep(2)
            while not (start_btn_location := check_image_presence(start_btn_img)):
                time.sleep(0.2)
            click_random_within_image(start_btn_location)
            setlog("Start button clicked", 'info')

            while not (trash_btn_location := check_image_presence(trash_btn_img)):
                time.sleep(0.5)
            click_random_within_image(trash_btn_location) # click trash button
            setlog("Trash button clicked", 'info')

            while not (ok_btn_location := check_image_presence(ok_btn_img)):
                setlog("Waiting for OK button to appear...", 'info')
                time.sleep(0.5)
            click_random_within_image(ok_btn_location)
            setlog("OK button clicked", 'info')

            if gem_cooldown:
                while not (gem_cd_location := check_image_presence(gem_cd_img)):
                    time.sleep(0.5)
                click_random_within_image(gem_cd_location)
                time.sleep(2.5)
                do_click(547, 351) # click okay button
            else:
                do_click(867, 262) # click away to close clan games window
                do_click(867, 262) # click away just to be sure
            setlog("Challenge purged", 'success')
            purged = True
            if purge_once:
                setlog("Switch account is enabled", 'info')
                setlog("Only purging 1 challenge, exiting purge_challenge() now", 'info')
                break
        else:
            setlog("No more home village challenge", "success")
            setlog("Exiting purge now...", "info")
            break
        time.sleep(3)

    if purged:
        # do_click(867, 262) # click away to close clan games window
        # setlog("click away", "info")
        return True
    else:
        setlog("No challenge purged", "warning")
        # do_click(867, 262) # click away to close clan games window
        # setlog("click away", "info")
        return False

cg_points_full = False

def pick_challenge(debug=False):
    global cg_points_full
    global assets_path

    cg_points_full = assets_path + '\\cg_points_full.png'
    if find_image_within_window(cg_points_full):
        setlog("CLAN GAMES COMPLETED", "info")
        cg_points_full = True
        return False
    start_btn_img = assets_path + '\\start_btn.png'
    trash_btn_img = assets_path + '\\trash_btn.png'
    ok_btn_img = assets_path + '\\okay_btn.png'
    gem_cd_img = assets_path + '\\gem_cd.png'

    bb_challenge = assets_path + '\\bb_assets\\bb_challenge.png'
    challenges_to_purge = [
        assets_path + '\\cg_bb\\boxer_giant_punch_up.png',
        assets_path + '\\cg_bb\\riding_n_gliding.png',
        assets_path + '\\cg_bb\\bomber_blow_em_up.png',
        assets_path + '\\cg_bb\\wall_wipe_out.png',
        assets_path + '\\cg_bb\\XBow_Explosion.png',
        assets_path + '\\cg_bb\\electrofire_crackle.png',
    ]

    def remove_challenge(challenge_img):
        setlog(f"Found an undoable challenge - '{challenge_img}'", "warning")
        setlog("Removing it now...", "info")
        click_random_within_image(check_image_presence(challenge_img))

        while not (start_btn_location := check_image_presence(start_btn_img)):
            time.sleep(0.5)
        click_random_within_image(start_btn_location)
        time.sleep(1)
        while not (trash_btn_location := check_image_presence(trash_btn_img)):
            time.sleep(0.5)
        click_random_within_image(trash_btn_location)

        while not (ok_btn_location := check_image_presence(ok_btn_img)):
            time.sleep(0.2)
        click_random_within_image(ok_btn_location)

        # TODO make gemming the purge an option, pass it as parameter, temporarily gem it because we are rushing cg right now
        # TODO maybe make a GUI "gem unwanted challenges" option
        while not (gem_cd_location := check_image_presence(gem_cd_img)):
            time.sleep(0.2)
        click_random_within_image(gem_cd_location)
        # TODO --------------------------------------------------------
        while not (ok_btn_location := check_image_presence(ok_btn_img)):
            time.sleep(0.2)
        click_random_within_image(ok_btn_location)

        setlog("Challenge removed", "success")
        setlog("Searching for available BB challenge again...", "info")

    count = 0
    while True:
        count += 1
        if count == 10:
            setlog("Purged 10 times, no BB challenge found", "warning")
            return False

        for challenge_img in challenges_to_purge:
            if find_image_within_window(challenge_img):
                remove_challenge(challenge_img)

        time.sleep(2)
        if find_image_within_window(bb_challenge):
            if click_random_within_image(check_image_presence(bb_challenge, confidence=0.9)):
                setlog("BB challenge found", "success")

                while not (start_btn_location := check_image_presence(start_btn_img)):
                    time.sleep(0.5)
                click_random_within_image(start_btn_location)
                setlog("BB challenge started", "success")
                time.sleep(0.5)
                do_click(867, 262)  # Click away to close clan games window
                do_click(867, 262)  # Click away to close clan games window
                return True
            else:
                return False
        time.sleep(2)

def open_cg_window():
    global assets_path

    img = assets_path + '\\cg_cart2.png'
    if find_image(img):
        setlog("found clan games cart", "success")
        setlog("Opening clan games window", "info")
        time.sleep(1)
        clan_games_location = check_image_presence(img, confidence=0.8)
        click_random_within_image(clan_games_location)
        return True
    else:
        setlog("Failed to find clan games cart", "error")
        setlog("Retrying...", "info")
        scroll_to_zoom((716, 117), 10)
        time.sleep(1)
        click_drag(716, 117, 419, 376)
        # try again
        if find_image(img):
            setlog("found on 2nd try", "success")
            time.sleep(1)
            img2 = assets_path + '\\cg_cart2.png'
            clan_games_location2 = check_image_presence(img2, confidence=0.8)
            click_random_within_image(clan_games_location2) # open clan games window
            return True
    return False

def switch_acc_purge(skip_acc_num=0, skip_acc_num2=0):
    global assets_path
    count = 0
    while 1:
        count += 1

        if count == 5: # change here how many accounnts you want to switch
            setlog("Purged 5 times, going back to the account", 'info')
            switch_acc(skip_acc_num)
            is_army_btn_visible()
            return True
        # if count > 21 or count == skip_acc_num:
        if count == skip_acc_num or count == skip_acc_num2:
            count += 1
            switch_acc(count)
        else:
            switch_acc(count)
        is_army_btn_visible()

        scroll_to_zoom((570, 274), 10) # zoom out first
        click_drag(473, 268, 372, 459)

        time.sleep(3)
        cg_cart_img = assets_path + '\\cg_cart3.png'
        if (cg_cart_location := check_image_presence(cg_cart_img)):
            click_random_within_image(cg_cart_location)
            setlog("Cart found, switch_acc_purge", 'info')
        else:
            setlog("Cart not found, exiting script...", 'error')
            do_click(280, 119) # just click the cart
            do_click(226, 131) # click it again

        # cg_indicator_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\cg_indicator.png'
        # while not check_image_presence(cg_indicator_img):
        #     setlog("Waiting for CG window to open...", 'info')
        #     time.sleep(0.5)
        time.sleep(5)
        setlog("Clan Games window is open", 'info')

        setlog("Start purging challenge...", 'info')
        time.sleep(3)
        purge_challenge(purge_once=True)

def cg_mode_loop(gem_cooldown=False, is_2_camps=False, collect_cart=True):

    global assets_path

    challenge_completed_img = assets_path + '\\bb_assets\\challenge_completed2.png'
    bb_atk_btn_img = assets_path + '\\bb_assets\\bb_atk_btn.png'

    cart_w_elixir = assets_path + '\\bb_assets\\cart_with_elixir.png'
    btn_collect_elixir_cart = assets_path + '\\bb_assets\\collect_elixir_cart.png'
    cart_full_img = assets_path + '\\bb_assets\\elixir_cart_full.png'
    cart2_img = assets_path + '\\bb_assets\\elixir_cart2.png'

    while 1:
        #* Check if cg chellenge has been completed
        while not find_image_within_window(challenge_completed_img, confidence=0.7):
            time.sleep(2)
            setlog("Challenge not completed yet", "info")
            setlog("Continuing to attack", "info")
            #* if not completed then attack
            attack_BB(is_2_camps=is_2_camps)
            time.sleep(1)
            #* This loop is for when the battle is finish, we look for atk button to know if we are back on builder base
            setlog("Waiting for builder base attack button to appear", "info")
            for i in range(20): # 0.3 x 20 = 6 seconds wait time
                time.sleep(0.3)
                if find_image_within_window(bb_atk_btn_img):
                    setlog("We are back at builder base!", "success")
                    do_click(867, 262)
                    do_click(867, 262)
                    break

            star_bonus_img = assets_path + '\\bb_assets\\star_bonus.png'
            if find_image_within_window(star_bonus_img):
                setlog("Star bonus found, clicking now", 'info')
                do_click(867, 262)

            # for i in range(100): # 0.1 x 100 = 10 seconds wait time
            #     time.sleep(0.1)
            #     if find_image_within_window(challenge_completed_img, confidence=0.7):
            #         break

            # #* Check cart for elixir then collect it
            # scroll_to_zoom((716, 117), 10)
            # click_drag(854, 271, 700, 429)
            # setlog("Checking cart for elixir...", "info")
            # time.sleep(3)
            # if click_random_within_image(check_image_presence(cart_full_img, confidence=0.7)) or click_random_within_image(check_image_presence(cart2_img, confidence=0.7)):
            #     while not find_image_within_window(btn_collect_elixir_cart, confidence=0.7):
            #         time.sleep(0.2)
            #     if click_random_within_image(check_image_presence(btn_collect_elixir_cart, confidence=0.7)):
            #         setlog("Collected elixir cart", "success")
            #         time.sleep(1)
            #         do_click(867, 262) # click away
            #         do_click(867, 262)
            #     else:
            #         setlog("Failed to collect elixir cart, something wrong with collect_elixir_cart", "error")
            # else:
            #     setlog("Cart does not have elixir yet", "info")

        else:
            #* if challenge completed then click the "challenge completed" button
            setlog("Challenge completed", "success")
            click_random_within_image(check_image_presence(challenge_completed_img, confidence=0.7))
            # time.sleep(5)
            # purge_challenge()
            time.sleep(4)
            #* Try to pick a new challenge
            if pick_challenge():
                do_click(891, 241) # click away
                do_click(891, 241) # click away
                continue #* if pick_challenge is successful then continue to the next iteration
            else:
                go_to_bb(go_back_main=True) # go to main village
                time.sleep(1)
                switch_acc_purge(skip_acc_num=6, skip_acc_num2=1)
                scroll_to_zoom((570, 274), 10)
                click_drag(473, 268, 372, 459)

                time.sleep(2)
                cg_cart_img = assets_path + '\\cg_cart3.png'
                if (cg_cart_location := check_image_presence(cg_cart_img)):
                    click_random_within_image(cg_cart_location)
                    setlog("Cart found, cg_mode_loop", 'info')
                else:
                    setlog("Cart not found, exiting script...", 'error')
                    do_click(280, 119) # just click the cart
                    do_click(226, 131) # click it again
                # cg_indicator_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\cg_indicator.png'
                # while not check_image_presence(cg_indicator_img):
                #     setlog("Waiting for CG window to open...", 'info')
                #     time.sleep(0.5)
                time.sleep(5)
                if pick_challenge():
                    do_click(891, 241)
                    do_click(891, 241)
                    continue
                else:
                    purge_challenge(gem_cooldown=True) # if no bb challenge even tho we purged 10 times using switch accounts then make it gem the purge until bb challenge is available
                    time.sleep(3)
                    pick_challenge()
                    do_click(891, 241) # click away
                    do_click(891, 241) # click away

                go_to_bb() # go back to bb after purging and picking challenge
                time.sleep(1)
                continue # continue the loop

                # purge_challenge(gem_cooldown=gem_cooldown)
                # time.sleep(3)
                # pick_challenge()
                # do_click(891, 241) # click away
                # do_click(891, 241) # click away

                # #* Check cart for elixir then collect it
                # scroll_to_zoom((716, 117), 10)
                # click_drag(854, 271, 700, 429)
                # setlog("Checking cart for elixir...", "info")
                # time.sleep(3)
                # if click_random_within_image(check_image_presence(cart_full_img, confidence=0.7)) or click_random_within_image(check_image_presence(cart2_img, confidence=0.7)):
                #     while not find_image_within_window(btn_collect_elixir_cart, confidence=0.7):
                #         time.sleep(0.2)
                #     if click_random_within_image(check_image_presence(btn_collect_elixir_cart, confidence=0.7)):
                #         setlog("Collected elixir cart", "success")
                #         time.sleep(1)
                #         do_click(867, 262) # click away
                #         do_click(867, 262)
                #     else:
                #         setlog("Failed to collect elixir cart, something wrong with collect_elixir_cart", "error")
                # else:
                #     setlog("Cart does not have elixir yet", "info")

def play_sound():
    from os import environ
    environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
    import pygame
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

def cg_mode_loop_2(assets_path, is_2_camps=False):

    challenge_completed_img = assets_path + '\\bb_assets\\challenge_completed2.png'
    bb_atk_btn_img = assets_path + '\\bb_assets\\bb_atk_btn.png'

    btn_collect_elixir_cart = assets_path + '\\bb_assets\\collect_elixir_cart.png'
    cart_full_img = assets_path + '\\bb_assets\\elixir_cart_full.png'
    cart2_img = assets_path + '\\bb_assets\\elixir_cart2.png'

    # is_challenge_complete = False
    while 1:
        # if is_challenge_complete:
        #     is_challenge_complete = False # reset the flag
        #     setlog("--- CHALLENGE COMPLETED ---", "success")
        #     setlog("PLEASE PICK A NEW CHALLENGE", "info")
        #     break
        #* Check if cg chellenge has been completed
        while not find_image_within_window(challenge_completed_img, confidence=0.7):
            time.sleep(2)
            setlog("Challenge not completed yet", "info")
            setlog("Continuing to attack", "info")
            #* if not completed then attack
            attack_BB(is_2_camps=is_2_camps)
            time.sleep(1)
            #* This loop is for when the battle is finish, we look for atk button to know if we are back on builder base
            setlog("Waiting for builder base attack button to appear", "info")
            for i in range(20): # 0.3 x 20 = 6 seconds wait time
                time.sleep(0.3)
                if find_image_within_window(bb_atk_btn_img):
                    setlog("We are back at builder base!", "success")
                    do_click(867, 262)
                    do_click(867, 262)
                    break
            #     if (challenge_completed_location := check_image_presence(challenge_completed_img, confidence=0.7)):
            #         click_random_within_image(challenge_completed_location)
            #         is_challenge_complete = True
            #         play_sound()
            #         break

            # if is_challenge_complete:
            #     # is_challenge_complete = False # reset the flag
            #     break

        else:
            #* if challenge completed then click the "challenge completed" button
            setlog("Challenge completed", "success")
            click_random_within_image(check_image_presence(challenge_completed_img, confidence=0.7))
            time.sleep(5)
            purge_challenge(gem_cooldown=True)
            time.sleep(4)
            #* Try to pick a new challenge
            if pick_challenge():
                do_click(891, 241) # click away
                do_click(891, 241) # click away

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

                continue #* if pick_challenge is successful then continue to the next iteration
            else:
                purge_challenge()
                time.sleep(3)
                pick_challenge()
                do_click(891, 241) # click away
                do_click(891, 241) # click away

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

def cg_mode_loop_3(assets_path, is_2_camps=False):

    global cg_points_full
    print(cg_points_full)
    if cg_points_full:
        setlog("cg_points_full is True", "info")
        return

    challenge_completed_img = assets_path + '\\bb_assets\\challenge_completed2.png'
    bb_atk_btn_img = assets_path + '\\bb_assets\\bb_atk_btn.png'

    btn_collect_elixir_cart = assets_path + '\\bb_assets\\collect_elixir_cart.png'
    cart_full_img = assets_path + '\\bb_assets\\elixir_cart_full.png'
    cart2_img = assets_path + '\\bb_assets\\elixir_cart2.png'

    # is_challenge_complete = False
    while 1:

        #* Check if cg chellenge has been completed
        while not find_image_within_window(challenge_completed_img, confidence=0.7):
            time.sleep(2)
            setlog("Challenge not completed yet", "info")
            setlog("Continuing to attack", "info")
            #* if not completed then attack
            attack_BB(is_2_camps=is_2_camps)
            time.sleep(1)
            #* This loop is for when the battle is finish, we look for atk button to know if we are back on builder base
            setlog("Waiting for builder base attack button to appear", "info")
            for i in range(20): # 0.3 x 20 = 6 seconds wait time
                time.sleep(0.3)
                if find_image_within_window(bb_atk_btn_img):
                    setlog("We are back at builder base!", "success")
                    do_click(867, 262)
                    do_click(867, 262)
                    break
            #     if (challenge_completed_location := check_image_presence(challenge_completed_img, confidence=0.7)):
            #         click_random_within_image(challenge_completed_location)
            #         is_challenge_complete = True
            #         play_sound()
            #         break

            # if is_challenge_complete:
            #     # is_challenge_complete = False # reset the flag
            #     break

        else:
            #* if challenge completed then click the "challenge completed" button
            setlog("Challenge completed", "success")
            click_random_within_image(check_image_presence(challenge_completed_img, confidence=0.7))
            time.sleep(5)
            purge_challenge()
            time.sleep(4)
            #* Try to pick a new challenge
            if pick_challenge():
                do_click(891, 241) # click away
                do_click(891, 241) # click away

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

                continue #* if pick_challenge is successful then continue to the next iteration
            else:
                purge_challenge()
                time.sleep(3)
                pick_challenge()
                do_click(891, 241) # click away
                do_click(891, 241) # click away

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

if __name__ == '__main__':
    cg_mode_loop_3(assets_path, is_2_camps=False)

    # directory_path = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\bb_assets\bb_armycamp'
    # matched_image, final_confidence, locations = find_multiple_images_in_directory(directory_path)

    # if matched_image:
    #     setlog(f"The matched image is: {matched_image} (Confidence: {final_confidence:.2f})", "info")
    #     setlog(f"Total matches found: {len(locations)}", "info")
    # else:
    #     setlog("No images were matched", "error")
