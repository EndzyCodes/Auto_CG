import time, random
from ...Functions.image_detection import (
    check_image_presence,
    click_random_within_image,
    find_image_in_directory,
    find_image
)
from ...Functions.click_utils import do_click
from ...Functions.logging_utils import setlog
from ...config import assets_path
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

def is_army_btn_visible(click=False):
    global assets_path

    img = assets_path + '\\army_btn.png'

    setlog("Waiting for army tab to appear", "info")
    while  not check_image_presence(img, confidence=0.8):
        time.sleep(0.3)

    setlog("Army tab found", "success")
    do_click(867, 262)
    do_click(867, 262)
    do_click(867, 262)
    if click:
        if click_random_within_image(check_image_presence(img, confidence=0.8)):
            time.sleep(1)
            setlog("Clicked on army tab", "success")
            return True
        else:
            setlog("No army tab", "info")
            return False

    return True

def boost_clock_tower(assets_path):
    directory_path = assets_path + '\\bb_assets\\clock_tower'

    clock_tower_found = find_image_in_directory("find clock tower", directory_path, confidence_range=(0.8, 0.6))
    free_boost_button_found = find_image_in_directory("find free boost button", directory_path, confidence_range=(0.8, 0.6))
    boost_button_found = find_image_in_directory("find boost button", directory_path, confidence_range=(0.8, 0.6))

    if clock_tower_found:
        setlog("Clock tower found", "success")
    else:
        setlog("Clock tower not found", "warning")

    if free_boost_button_found:
        setlog("Found free boost button", "success")
    else:
        setlog("Boost button not found", "warning")

    if boost_button_found:
        setlog("Boosted clock tower", "success")
    else:
        setlog("Boost button not found", "warning")

    # if (clock_tower_location := check_image_presence(clock_tower_img, confidence=0.8)):
    #     click_random_within_image(clock_tower_location)
    #     time.sleep(1)
    #     if (boost_btn_location := check_image_presence(boost_btn_img, confidence=0.8)):
    #         click_random_within_image(boost_btn_location)
    #         setlog("Boosted clock tower", "success")
    #         do_click(905, 283)  # click away
    #         do_click(905, 283)  # click away
    #         return True
    #     else:
    #         setlog("Boost button not found", "warning")
    #         do_click(905, 283)  # click away
    #         do_click(905, 283)  # click away
    #         return False
    # else:
    #     setlog("Clock tower not found", "warning")
    #     return False

def bb_collect_resource(assets_path):
    bb_gold = assets_path + '\\bb_assets\\bb_gold.png'
    bb_elixir = assets_path + '\\bb_assets\\bb_elixir.png'
    bb_gem = assets_path + '\\bb_assets\\bb_gem.png'

    resources_imges = [bb_gold, bb_elixir, bb_gem]
    random.shuffle(resources_imges)
    collected_resources = False

    for resource_img in resources_imges:
        if (resource_location := check_image_presence(resource_img, confidence=0.8)):
            click_random_within_image(resource_location)
            resource_name = resource_img.split('\\')[-1].split('.')[0].capitalize()
            setlog(f"Collected {resource_name}", "info")
            collected_resources = True

    if collected_resources:
        setlog("Resources collected", "info")
    else:
        setlog("No resources collected", "info")

    return collected_resources

def collect_gem_box(assets_path):
    gem_box_img = assets_path + '\\mv_assets\\gem_box.png'
    if (gem_box_location := check_image_presence(gem_box_img, confidence=0.8)):
        click_random_within_image(gem_box_location)
        time.sleep(1)
        do_click(467, 449)
        setlog("Collected gem box", "success")
        do_click(905, 283)  # click away
        do_click(905, 283)  # click away
        return True
    else:
        setlog("Gem box not found", "warning")
        return False

def collect_clan_capital_gold(assets_path):
    clan_capital_gold_img = assets_path + '\\mv_assets\\clan_capital_gold.png'
    collect_btn_img = assets_path + '\\mv_assets\\collect_btn.png'

    if find_image(clan_capital_gold_img):
        if (collect_btn_location := check_image_presence(collect_btn_img, confidence=0.8)):
            click_random_within_image(collect_btn_location)
            setlog("Collected clan capital gold", "success")
            return True
        else:
            setlog("Collect button not found", "error")
            return False
    else:
        setlog("Clan capital gold not found", "warning")
        return False

def collect_resources(assets_path):
    gold_img = assets_path + '\\gold.png'
    elixir_img = assets_path + '\\elixir.png'
    dark_elixir_img = assets_path + '\\mv_funcs\\dark_elixir.png'

    resources_imges = [gold_img, elixir_img, dark_elixir_img]
    random.shuffle(resources_imges)
    collected_resources = False

    for resource_img in resources_imges:
        if (resource_location := check_image_presence(resource_img, confidence=0.8)):
            click_random_within_image(resource_location)
            resource_name = resource_img.split('\\')[-1].split('.')[0].capitalize()
            setlog(f"Collected {resource_name}", "info")
            collected_resources = True

    if collected_resources:
        setlog("Resources collected", "info")
    else:
        setlog("No resources collected", "info")

    return collected_resources
