# src/features/clan_games/main.py
from .cg_utils import (
    cg_mode_loop,
    cg_mode_loop_2,
    cg_mode_loop_3
)
from ...config import assets_path

def run_clan_games(mode=3, is_2_camps=False):
    if mode == 1:
        cg_mode_loop(assets_path, is_2_camps=is_2_camps)
    elif mode == 2:
        cg_mode_loop_2(assets_path, is_2_camps=is_2_camps)
    else:
        cg_mode_loop_3(assets_path, is_2_camps=is_2_camps)

if __name__ == '__main__':
    run_clan_games(mode=3, is_2_camps=False)
