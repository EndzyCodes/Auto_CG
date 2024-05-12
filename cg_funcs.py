
from Functions import (
    click_random_within_image,
    check_image_presence,
    find_image_within_window,
    find_image,

    do_click,
    click_drag,
    scroll_to_zoom,

    setlog
)
from bb_funcs import attack_BB
import time

def purge_challenge(gem_cooldown=False, debug=False):

    ok_btn_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\okay_btn.png'
    gem_cd_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\gem_cd.png'

    purged = False
    start_btn_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\start_btn.png'
    trash_btn_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\trash_btn.png'
    home_vill_challenge_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\home_vill_challenge.png'
    running_challenge_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\running_challenge.png'
    challenge_cooldown_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\challenge_cooldown.png'
    # bb_vill_challenge_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\bb_vill_challenge.png'

    while 1:
        if find_image_within_window(home_vill_challenge_img):
            setlog("Home Village Challenge found", "success")
            click_random_within_image(check_image_presence(home_vill_challenge_img, confidence=0.8))

            while not find_image_within_window(start_btn_img, confidence=0.8):
                time.sleep(0.2)
            click_random_within_image(check_image_presence(start_btn_img, confidence=0.8))

            while not find_image_within_window(trash_btn_img):
                time.sleep(0.5)
            click_random_within_image(check_image_presence(trash_btn_img)) # click trash button

            time.sleep(3)
            do_click(537, 344) # click okay button

            if gem_cooldown:
                while not find_image_within_window(gem_cd_img):
                    time.sleep(0.2)
                click_random_within_image(check_image_presence(gem_cd_img))
                time.sleep(2.5)
                do_click(547, 351) # click okay button
            else:
                do_click(867, 262) # click away to close clan games window
                do_click(867, 262) # click away just to be sure
            setlog("Challenge purged", 'success')
            purged = True
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

def pick_challenge(debug=False):
    start_btn_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\start_btn.png'
    trash_btn_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\trash_btn.png'
    ok_btn_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\okay_btn.png'
    gem_cd_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\gem_cd.png'

    bb_challenge = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\bb_assets\bb_challenge.png'
    challenge_images = [
        r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\cg_bb\boxer_giant_punch_up.png',
        r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\cg_bb\riding_n_gliding.png',
        r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\cg_bb\bomber_blow_em_up.png'
    ]

    def remove_challenge(challenge_img):
        setlog(f"Found an undoable challenge - '{challenge_img}'", "warning")
        setlog("Removing it now...", "info")
        click_random_within_image(check_image_presence(challenge_img))

        while not find_image_within_window(start_btn_img, confidence=0.8):
            time.sleep(0.2)
        click_random_within_image(check_image_presence(start_btn_img, confidence=0.8))

        while not find_image_within_window(trash_btn_img):
            time.sleep(0.5)
        click_random_within_image(check_image_presence(trash_btn_img))  # Click trash button

        while not find_image_within_window(ok_btn_img):
            time.sleep(0.2)
        click_random_within_image(check_image_presence(ok_btn_img))

        # TODO make gemming the purge an option, pass it as parameter, temporarily gem it because we are rushing cg right now
        while not find_image_within_window(gem_cd_img):
            time.sleep(0.2)
        click_random_within_image(check_image_presence(gem_cd_img))
        # TODO --------------------------------------------------------
        while not find_image_within_window(ok_btn_img):
            time.sleep(0.2)
        click_random_within_image(check_image_presence(ok_btn_img))

        setlog("Challenge removed", "success")
        setlog("Searching for available BB challenge again...", "info")

    while True:
        for challenge_img in challenge_images:
            if find_image_within_window(challenge_img):
                remove_challenge(challenge_img)

        time.sleep(2)
        if find_image_within_window(bb_challenge):
            if click_random_within_image(check_image_presence(bb_challenge, confidence=0.9)):
                setlog("BB challenge found", "success")

                while not  click_random_within_image(check_image_presence(start_btn_img, confidence=0.8)):
                    time.sleep(0.2)
                setlog("BB challenge started", "success")
                time.sleep(0.5)
                do_click(867, 262)  # Click away to close clan games window
                do_click(867, 262)  # Click away to close clan games window
                return True
            else:
                return False
        time.sleep(2)

def open_cg_window():

    img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\cg_cart2.png'
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
            img2 = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\cg_cart2.png'
            clan_games_location2 = check_image_presence(img2, confidence=0.8)
            click_random_within_image(clan_games_location2) # open clan games window
            return True
    return False

def cg_mode_loop(gem_cooldown=False):
    challenge_completed_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\bb_assets\challenge_completed.png'
    bb_atk_btn_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\bb_assets\bb_atk_btn.png'

    cart_w_elixir = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\bb_assets\cart_with_elixir.png'
    btn_collect_elixir_cart = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\bb_assets\collect_elixir_cart.png'
    cart_full_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\bb_assets\elixir_cart_full.png'
    cart2_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\bb_assets\elixir_cart2.png'

    while 1:
        #* Check if cg chellenge has been completed
        while not find_image_within_window(challenge_completed_img, confidence=0.8):
            time.sleep(1)
            setlog("Challenge not completed yet", "info")
            setlog("Continuing to attack", "info")
            #* if not completed then attack
            attack_BB()
            time.sleep(1)
            #* This loop is for when the battle is finish, we look for atk button to know if we are back on builder base
            setlog("Waiting for builder base attack button to appear", "info")
            for i in range(20):
                time.sleep(0.5)
                if find_image_within_window(bb_atk_btn_img):
                    setlog("We are back at builder base!", "success")
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

        else:
            #* if challenge completed then click the "challenge completed" button
            setlog("Challenge completed", "success")
            click_random_within_image(check_image_presence(challenge_completed_img, confidence=0.8))
            # time.sleep(5)
            # purge_challenge()
            time.sleep(4)
            #* Try to pick a new challenge
            if pick_challenge():
                do_click(891, 241) # click away
                do_click(891, 241) # click away
                continue #* if pick_challenge is successful then continue to the next iteration
            else:
                purge_challenge(gem_cooldown=gem_cooldown)
                time.sleep(3)
                pick_challenge()
                do_click(891, 241) # click away
                do_click(891, 241) # click away
                continue
