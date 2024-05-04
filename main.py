# user intruction: manually start a challenge then go to builder base then run the script
from GUI import ClashOfClansBotGUI
from Functions import *
from bb_funcs import bb_attack_time_limit
from PyQt6.QtWidgets import QApplication


#TODO - make it save the options you checked in the GUI so you don't have to check it again when you run the script
#TODO make it pick a challenge then make it go to bb, so me/user can run the script
#TODO make it switch account if builder base storages are full

def test():
    donate_btn_region = (165, 286, 119, 97) # x, y, width, height

    donate_btn_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\donate_assets\donate_btn.png'
    try:
        while 1:
            if click_random_within_image(check_image_presence(donate_btn_img, region=donate_btn_region)):
                print("I see it")
            else:
                print("I don't see it")
            time.sleep(1)
    except KeyboardInterrupt:
        print("User interrupted script")
        exit()

if __name__ == "__main__":

    # app = QApplication([])
    # ex = ClashOfClansBotGUI()
    # ex.show() # show the GUI
    # app.exec() # start the application

    # bb_attack_time_limit()

    test()
