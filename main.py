# user intruction: manually start a challenge then go to builder base then run the script
from GUI import ClashOfClansBotGUI
from Functions import *
from mv_funcs import is_army_btn_visible, main_village_attack_loop, EdragLoons_strat
from bb_funcs import bb_attack_time_limit, bb_attack_loop, attack_BB, bb_return_home, go_to_bb, BB_is_army_btn_visible
from cg_funcs import purge_challenge, switch_acc_purge
from PyQt6.QtWidgets import QApplication


#TODO - make it save the options you checked in the GUI so you don't have to check it again when you run the script
#TODO make it pick a challenge then make it go to bb, so me/user can run the script
#TODO make it switch account if builder base storages are full


def request_troops():

    region_trash_btn = (421, 355, 105, 43)

    trash_btn_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\donate_assets\trash_btn.png'
    ok_btn_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\donate_assets\ok_btn.png'

    if (trash_btn_location := check_image_presence(trash_btn_img, region=region_trash_btn)):
        setlog("Found troops in cc, removing troops now")
        click_random_within_image(trash_btn_location)
        time.sleep(1)
        if (ok_btn_location := check_image_presence(ok_btn_img)):
            click_random_within_image(ok_btn_location)
            do_click(734, 467) # click request button
            time.sleep(1)
            do_click(551, 402) # click send button
            setlog("Troop request successfully sent!", 'info')
    else:
        setlog("No troops in cc, skip click trash", 'info')
        do_click(734, 467) # click request button
        time.sleep(1)
        do_click(551, 402) # click send button
        setlog("Troop request successfully sent!", 'info')

def train_loons():

    do_click(41, 420) # click army tab
    time.sleep(1)
    do_click(680, 98) # click Quick train tab
    time.sleep(1)
    do_click(740, 277) # click "train" on the first army comp

    time.sleep(1)
    ok_btn_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\donate_assets\ok_btn.png'

    ok_btn_location = check_image_presence(ok_btn_img)

    if ok_btn_location:
        setlog("Ok button found, clicking", "info")
        click_random_within_image(ok_btn_location)
        do_click(867, 262) # click away to close army indow
        # return True
    else:
        do_click(867, 262) # click away to close army window
    return True

def donate_troops():
    donate_btn_region = (189, 421, 89, 67) # x, y, width, height
    donate_btn_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\donate_assets\donate_btn.png'

    if (donate_btn_location := check_image_presence(donate_btn_img, region=donate_btn_region)):
        click_random_within_image(donate_btn_location)
        setlog("Found a donate button, donating now!", "info")
        time.sleep(1.5)
        setlog("Donating loons...", "info")
        do_click(342, 213, click_hold=True) # click loons to donate
        do_click(723, 50) # click away to close donate window
        return True
    else:
        setlog("No more donate buttons found.", "info")
        setlog("Exiting donate loop to train troops...", "info")
        do_click(320, 262) # close clan chat
        time.sleep(1)
        return False

def donate_loop():

    count = 0
    while 1:
        count += 1

        if count > 21:
            count = 1
            switch_acc(count)
        else:
            switch_acc(count)
        is_army_btn_visible()

        time.sleep(1)
        scroll_to_zoom((570, 274), 10) # zoom out first
        do_click(46, 261) # open chat tab
        time.sleep(1)

        #* Donate loop
        for i in range(5): # only loop 5 times since it ill be 45 loons donated, our camp capacity is 50-60 loons
            if donate_troops():
                setlog("Donate count: "+ str(i+1), "info")
            else:
                time.sleep(1)
                break
            time.sleep(3)

        train_loons()

def find_multiple_img(img):
    window_rect = get_window_rect(window_title)
    locations = []
    try:
        for loc in pyautogui.locateOnWindow(img, confidence=0.8, title='Clash of Clans'):
            print(f"Found at: {loc}")
            # pyautogui.alert(text=loc, title='WARNING', button='OK')
            locations.append(loc)
            if len(locations) > 10:
                break

        if locations:
            for loc in locations:
                window_rect = get_window_rect(window_title)
                pyautogui.moveTo(loc.left, loc.top)
                time.sleep(1)
        else:
            print("Not Found")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":

    # bb_attack_loop(is_2_camps=True)

    # wall_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\test\wall_11.png'
    # unique_locations = set()
    # for i in range(10):
    #     location = pyautogui.locateOnWindow(wall_img, confidence=0.8, title='Clash of Clans')
    #     if location and (location.left, location.top) not in unique_locations:  # Check coordinates
    #         unique_locations.add((location.left, location.top))  # Save only coordinates
    #         pyautogui.click(location)
    # unique_locations = set()

    # if not unique_locations:
    #     print("Image not found")

    do_click(41, 420, "hello") # click army tab

    # app = QApplication([])
    # ex = ClashOfClansBotGUI()
    # ex.show() # show the GUI
    # app.exec() # start the application

    # EdragLoons_strat()
