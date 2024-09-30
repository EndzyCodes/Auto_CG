# user intruction: manually start a challenge then go to builder base then run the script
# from backups.GUI.GUI import ClashOfClansBotGUI
# from PyQt6.QtWidgets import QApplication

from src.Features.clan_games.cg_main import run_clan_games
from src.Features.main_village.mv_main import run_main_village
from src.Features.builder_base.bb_main import run_builder_base
from src.Features.collect_resources.collect_res_main import run_auto_collect, test_collect_resources
from src.Features.donate_troops.donate_main import donate_loop
# from src.Features.attack.attack_utils import attack_loop
from src.Features.request_troops.request_main import run_request_troops
from src.Functions.logging_utils import setlog

from src.Functions.image_detection import find_and_highlight_all_images
from src.config import window_title
import pygetwindow as gw
from src.Functions.window_utils import get_window_rect

# Now you can use these functions directly:
# run_clan_games()
# run_main_village()
# run_builder_base()
# run_auto_collect()
# donate_loop()
# run_request_troops()


if __name__ == "__main__":
    # test_collect_resources()
    # print_coc_window_size()
    set_coc_window_size(1173, 689)

    directory_path = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\test2'
    output_path = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\test2\output'
