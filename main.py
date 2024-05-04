# user intruction: manually start a challenge then go to builder base then run the script
from GUI import ClashOfClansBotGUI
from Functions import *
from bb_funcs import bb_attack_time_limit
from PyQt6.QtWidgets import QApplication

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

#TODO - make it save the options you checked in the GUI so you don't have to check it again when you run the script
#TODO make it pick a challenge then make it go to bb, so me/user can run the script
#TODO make it switch account if builder base storages are full

if __name__ == "__main__":

    app = QApplication([])
    ex = ClashOfClansBotGUI()
    ex.show() # show the GUI
    app.exec() # start the application

    # bb_attack_time_limit()
