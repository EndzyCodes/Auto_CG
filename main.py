# user intruction: manually start a challenge then go to builder base then run the script
# from backups.GUI.GUI import ClashOfClansBotGUI
# from PyQt6.QtWidgets import QApplication

from src.Features.clan_games.cg_main import run_clan_games
from src.Features.main_village.mv_main import run_main_village
from src.Features.builder_base.bb_main import run_builder_base
from src.Features.collect_resources.collect_res_main import run_auto_collect
from src.Features.donate_troops.donate_main import donate_loop
# from src.Features.attack.attack_utils import attack_loop
from src.Features.request_troops.request_main import run_request_troops

# Now you can use these functions directly:
# run_clan_games()
# run_main_village()
# run_builder_base()
# run_auto_collect()
# donate_loop()
# run_request_troops()


if __name__ == "__main__":
    run_auto_collect()
