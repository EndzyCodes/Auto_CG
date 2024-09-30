from .mv_utils import main_village_attack_loop, atk_loop
from ...config import assets_path
def run_main_village(is_switch_acc=False, attack_mode='normal'):
    if attack_mode == 'normal':
        main_village_attack_loop(isSwitchAcc=is_switch_acc)
    elif attack_mode == 'loop':
        atk_loop(assets_path)  # You might need to import assets_path from .config
    else:
        raise ValueError("Invalid attack mode. Choose 'normal' or 'loop'.")

if __name__ == '__main__':
    run_main_village()
