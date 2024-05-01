# user intruction: manually start a challenge then go to builder base then run the script

from GUI import *

#TODO make it pick a challenge then make it go to bb, so me/user can run the script

if __name__ == "__main__":

    # bb_attack_loop()
    app = QApplication([])
    ex = ClashOfClansBotGUI()
    ex.show() # show the GUI
    app.exec() # start the application

#TODO - make it save the options you checked in the GUI so you don't have to check it again when you run the script
