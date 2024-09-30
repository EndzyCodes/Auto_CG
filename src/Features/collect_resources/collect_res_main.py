from .collect_res_utils import (
    boost_clock_tower,
    bb_collect_resource,
    collect_gem_box,
    collect_clan_capital_gold,
    collect_resources,
    is_army_btn_visible,
    boost_clock_tower,
)
from ...Functions.click_utils import scroll_to_zoom
from ...Features.builder_base.bb_utils import go_to_bb
from ...config import assets_path

def run_auto_collect(skip_acc_num=0):
    count = 0
    while True:
        count += 1
        if skip_acc_num == count:
            count += 1

        if count >= 21:
            count = 0
            print("max accounts reached")
            print("Resetting counter")

        is_army_btn_visible()
        scroll_to_zoom((716, 117), 10)
        collect_resources(assets_path)
        collect_gem_box(assets_path)
        collect_clan_capital_gold(assets_path)
        collect_gem_box(assets_path)

        if go_to_bb():
            bb_collect_resource(assets_path)
            boost_clock_tower(assets_path)
            go_to_bb(True)  # go back to main village

def test_collect_resources():
    boost_clock_tower(assets_path)

if __name__ == "__main__":
    test_collect_resources()
