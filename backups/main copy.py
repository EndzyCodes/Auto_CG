

from backups.Functions2 import *
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QPushButton, QGroupBox, QTabWidget

enable_attack = False
gem_cooldown = False

class ClashOfClansBotGUI(QWidget):
    global enable_attack
    global gem_cooldown

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        x_pos = 10
        self.setFixedSize(500, 500)  # Set the fixed size of the window (width, height)

        # Create a tab widget
        tab_widget = QTabWidget(self)
        tab_widget.setGeometry(10, 10, 450, 350)

        # Clan Games Tab
        clan_games_tab = QWidget()
        clan_games_layout = QVBoxLayout()
        clan_games_tab.setLayout(clan_games_layout)

        # Create a group box for gem settings
        gem_group_box = QGroupBox("Clan Games Settings", self)
        gem_group_box.setGeometry(25, 40, 200, 100) # x, y, width, height - Set position and size of the group box

        self.gemCooldownCheckbox = QCheckBox("Gem Challenge Cooldown", gem_group_box)
        self.gemCooldownCheckbox.move(x_pos, 20)

        self.clanGamesCheckbox = QCheckBox("Clan Games Mode", gem_group_box)
        self.clanGamesCheckbox.move(x_pos, 45)

        self.attackOnlyCheckbox = QCheckBox("Attack Only, No Clan Games", gem_group_box)
        self.attackOnlyCheckbox.move(x_pos, 70)

        tab_widget.addTab(clan_games_tab, "Clan Games")

        # BB Attack Tab
        bb_attack_tab = QWidget()
        bb_attack_layout = QVBoxLayout()
        bb_attack_tab.setLayout(bb_attack_layout)

        tab_widget.addTab(bb_attack_tab, "BB Attack")

        # Main Village Tab
        main_village_tab = QWidget()
        main_village_layout = QVBoxLayout()
        main_village_tab.setLayout(main_village_layout)

        tab_widget.addTab(main_village_tab, "Main Village")

        self.startButton = QPushButton("Start Bot", self)
        self.startButton.move(30, 420)
        self.startButton.resize(120, 40)

        self.setWindowTitle('Clash of Clans Bot Configuration')

    def startBot(self):
        gem_cooldown = self.gemCooldownCheckbox.isChecked()
        participate_in_clan_games = self.clanGamesCheckbox.isChecked()
        attack_only = self.attackOnlyCheckbox.isChecked()
        enable_attack = self.EnableAttackCheckbox.isChecked()

        print(f"Starting bot with configurations: Gem Cooldown: {gem_cooldown}, Clan Games: {participate_in_clan_games}, Attack Only: {attack_only}")

        # Here you would add the logic to start the bot with these configurations
        #* pass the variables to the functions that need them
        # Example: You might want to call bb_attack_loop() here or modify it to accept parameters based on the GUI settings
        gem_cooldown = gem_cooldown
        enable_attack = enable_attack

        main()

#* ----- CLICK FUNCTIONS -----
# def click(x, y):
#     pyautogui.click(x, y)

def random_click(x, y, rand_x_range=(5, 15), rand_y_range=(5, 15), clicks = 1, hold_duration_ms=0, debug = False):
    # random_click(1792, 290, (20,100), (20,89), 1, random.randint(100,200), debug=True)
    for i in range(clicks):
        # Generate random offsets between 5 and 10 pixels
        random_offset_x = random.randint(*rand_x_range)
        random_offset_y = random.randint(*rand_y_range)

        # Calculate the new x and y coordinates with random offsets
        random_x = x + random_offset_x
        random_y = y + random_offset_y

        if keyboard.is_pressed('q'):
            break

        if debug: # if debug is true then print these
            print("Click: ", i + 1) # print current click, + 1 to start counting on 1 and not start 0
            print("Clicking at coords:", random_x, random_y)
            print("offsets: ", random_offset_x, random_offset_y)
            print("Hold duration: ", hold_duration_ms)

        pyautogui.mouseDown(random_x, random_y)
        time.sleep(hold_duration_ms / 1000)
        pyautogui.mouseUp()

def click_close():
    close_btn_img_path = r'C:\Users\Mark\Desktop\coc\Images\close_btn.png'
    close_btn_present = check_image_presence(close_btn_img_path, confidence=0.8)
    if close_btn_present:
        click_random_within_image(close_btn_present)
    else:
        print("Close button not found.")


# def scroll_acc(move_to=(0,0), drag_to=(0,0)):
#     delay = random.uniform(0.5,0.8)
#     duration = random.uniform(0.4, 0.9)
#     duration_move_to_ = random.uniform(0.8, 1.5)

#     pyautogui.moveTo(move_to[0], move_to[1], duration=duration_move_to_)
#     time.sleep(delay)
#     pyautogui.dragTo(pyautogui.position(drag_to[0], drag_to[1]), duration=duration, button='left')  # Drag the mouse to the middle of the screen

def is_army_btn_visible():

    img = r'C:\Users\Mark\Desktop\AutoAttackBB\assets\army_btn.png'

    count = 0
    while 1:
        if not check_image_presence(img, confidence=0.8):
            time.sleep(0.3)
            count += 1
            if count == 1: setlog("Waiting for army tab to appear", "info")
        else:
            setlog("Army tab found", "success")
            return True
            # break

def check_daily_reward():
    img = r'C:\Users\Mark\Desktop\AutoAttackBB\assets\claim_btn.png'
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
    gold_img = r'C:\Users\Mark\Desktop\AutoAttackBB\assets\gold.png'
    elixir_img = r'C:\Users\Mark\Desktop\AutoAttackBB\assets\elixir.png'
    dark_elixir_img = r'C:\Users\Mark\Desktop\AutoAttackBB\assets\dark_elixir.png'

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

def open_cg_window():

    img = r'C:\Users\Mark\Desktop\AutoAttackBB\assets\cg_cart2.png'
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
            img2 = r'C:\Users\Mark\Desktop\AutoAttackBB\assets\cg_cart2.png'
            clan_games_location2 = check_image_presence(img2, confidence=0.8)
            click_random_within_image(clan_games_location2) # open clan games window
            return True
    return False

def main(skip_acc_num=0):
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
        if find_image_within_window(r'C:\Users\Mark\Desktop\AutoAttackBB\assets\daily_reward.png'):
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

def deploy_troops(sec_vill_battle=False):

    if sec_vill_battle:
        setlog("Deploying troops on the 2nd village battle ground", "info")
        setlog("Dropping loons", "info")
        click(165, 509) # click hero
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
        click(165, 509) # click hero
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

def return_home():
    return_home_btn_img = r'C:\Users\Mark\Desktop\AutoAttackBB\assets\bb_assets\return_home_btn.png'
    hero_ability_img = r'C:\Users\Mark\Desktop\AutoAttackBB\assets\bb_assets\hero_ability.png'

    count = 0
    timeout = 90  # timeout in seconds
    start_time = time.time()
    while not find_image_within_window(return_home_btn_img):
        count += 1
        if count == 1: setlog("Waiting for return home button to appear", "info")
        if time.time() - start_time > timeout:
            setlog("Something went wrong on detecting return home button", "error")
            break
        time.sleep(1)
        if find_image_within_window(hero_ability_img, confidence=0.9):
            if click_random_within_image(check_image_presence(hero_ability_img, confidence=0.9)):
                setlog("Hero ability is ready again, clicking it now", "info")

    count = 0

    # if find_image_within_window(return_home_btn_img):
    if click_random_within_image(check_image_presence(return_home_btn_img, confidence=0.8)):
        setlog("Clicked return home button", "success")
        return True
    else:
        setlog("Failed to click return home button", "error")
        return False
    # else:
    #     setlog("Return home button did not appear", "warning")

found_opponent = False
def attack_BB():
    global found_opponent
    get_coc_window("Clash of Clans")
    bb_atk_btn_img = r'C:\Users\Mark\Desktop\AutoAttackBB\assets\bb_assets\bb_atk_btn.png'
    if find_image_within_window(bb_atk_btn_img):
        if click_random_within_image(check_image_presence(bb_atk_btn_img, confidence=0.8)):
            setlog("Clicked attack button", "success")
            time.sleep(1.5)
        else:
            setlog("Failed to attack button", "error")
    else:
        setlog("Builder base attack button not found", "error")

    find_now_btn_img = r'C:\Users\Mark\Desktop\AutoAttackBB\assets\bb_assets\find_now_btn.png'
    if click_random_within_image(check_image_presence(find_now_btn_img, confidence=0.8)):
        setlog("Clicked find now button", "success")
        time.sleep(1.5)
    else:
        setlog("Failed to click find now button", "error")

    cancel_btn_img = r'C:\Users\Mark\Desktop\AutoAttackBB\assets\bb_assets\cancel_btn.png'
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

    return_home_btn_img = r'C:\Users\Mark\Desktop\AutoAttackBB\assets\bb_assets\return_home_btn.png'
    sec_vill_loon = r'C:\Users\Mark\Desktop\AutoAttackBB\assets\bb_assets\sec_vill_loon.png'
    hero_ability_img = r'C:\Users\Mark\Desktop\AutoAttackBB\assets\bb_assets\hero_ability.png'

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
        # balloon_troop = r'C:\Users\Mark\Desktop\AutoAttackBB\assets\bb_assets\balloon_troop.png'
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
            return_home()

def go_to_bb(go_back_main=False):

    boat_img = r'C:\Users\Mark\Desktop\AutoAttackBB\assets\bb_assets\boat.png'

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

def cg_loop():

    scroll_to_zoom((716, 117), 10)
    click_drag(716, 117, 419, 376)

    time.sleep(1)
    open_cg_window()

    if pick_challenge():
        pass
    else:
        purge_challenge()
        time.sleep(1)
        pick_challenge()

    time.sleep(1)
    go_to_bb()

    time.sleep(2)

    bb_attack_loop()


# user intruction: manually start a challenge then go to builder base then run the script
#TODO make it pick a challenge then make it go to bb, so me/user can run the script

    # click_drag(738, 369, 672, 439)
def bb_attack_loop(enable_attack=False):
    close_btn_img = r'C:\Users\Mark\Desktop\AutoAttackBB\assets\close_btn.png'
    bb_atk_btn_img = r'C:\Users\Mark\Desktop\AutoAttackBB\assets\bb_assets\bb_atk_btn.png'
    challenge_completed_img = r'C:\Users\Mark\Desktop\AutoAttackBB\assets\bb_assets\challenge_completed.png'
    cart_w_elixir = r'C:\Users\Mark\Desktop\AutoAttackBB\assets\bb_assets\cart_with_elixir.png'
    collect_elixir_cart = r'C:\Users\Mark\Desktop\AutoAttackBB\assets\bb_assets\collect_elixir_cart.png'
    cart_img = r'C:\Users\Mark\Desktop\AutoAttackBB\assets\bb_assets\cart.png'
    cart2_img = r'C:\Users\Mark\Desktop\AutoAttackBB\assets\bb_assets\cart2.png'

    if not enable_attack:
        setlog("Attack disabled", "info")
        return True
    else:
        setlog("Attack enabled", "info")
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
                if click_random_within_image(check_image_presence(cart_w_elixir, confidence=0.9)) or click_random_within_image(check_image_presence(cart2_img)):
                    while not find_image_within_window(collect_elixir_cart, confidence=0.9):
                        time.sleep(0.2)
                    if click_random_within_image(check_image_presence(collect_elixir_cart, confidence=0.9)):
                        setlog("Collected elixir cart", "success")
                        click(867, 262) # click away
                        click(867, 262)
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
                    click(891, 241) # click away
                    click(891, 241) # click away
                    continue #* if pick_challenge is successful then continue to the next iteration
                else:
                    purge_challenge()
                    time.sleep(3)
                    pick_challenge()
                    click(891, 241) # click away
                    click(891, 241) # click away
                    continue

def main():
    global enable_attack
    bb_attack_loop(enable_attack=enable_attack)

if __name__ == "__main__":

    # bb_attack_loop()
    app = QApplication([])
    ex = ClashOfClansBotGUI()
    ex.show() # show the GUI
    app.exec() # start the application
