from GUI import ClashOfClansBotGUI
from Functions import *
from mv_funcs import is_army_btn_visible, main_village_attack_loop, EdragLoons_strat
from bb_funcs import bb_attack_time_limit, bb_attack_loop, attack_BB, bb_return_home, go_to_bb, BB_is_army_btn_visible
from cg_funcs import purge_challenge, switch_acc_purge, pick_challenge
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":

    pick_challenge()