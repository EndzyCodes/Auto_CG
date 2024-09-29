from Functions import (
    click_random_within_image,
    check_image_presence,
    find_image_within_window,
    find_image,
    switch_acc,

    do_click,
    click_drag,
    scroll_to_zoom,

    switch_acc,

    setlog
)
from bb_funcs import go_to_bb
import random, time, pyautogui

assets_path = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets'

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

def collect_resources(assets_path):

    gold_img = assets_path + '\\gold.png'
    elixir_img = assets_path + '\\elixir.png'
    dark_elixir_img = assets_path + '\\dark_elixir.png'

    # Create a list of resource images
    resource_images = [gold_img, elixir_img, dark_elixir_img]

    # Randomize the order of resource collection
    random.shuffle(resource_images)

    collected_resources = False

    for resource_img in resource_images:
        resource_location = check_image_presence(resource_img, confidence=0.8)
        if find_image(resource_img):
            try:
                click_random_within_image(resource_location)
            except pyautogui.ImageNotFoundException:
                setlog(f"Image: {resource_img} not found", "info")
            resource_name = resource_img.split('\\')[-1].split('.')[0].capitalize()
            setlog(f"Collected {resource_name}", "info")
            collected_resources = True

    if collected_resources:
        setlog("Resources collected", "info")
    else:
        setlog("No resources collected", "info")

    return collected_resources

def boost_clock_tower(assets_path):
    clock_tower_img = assets_path + '\\bb_assets\\clock_tower.png'
    clocktower_boost_btn = assets_path + '\\bb_assets\\clocktower_boost_btn.png'
    clocktower_boost_btn2 = assets_path + '\\bb_assets\\clocktower_boost_btn2.png'

    if (clock_tower_location := check_image_presence(clock_tower_img, confidence=0.8)):
        if click_random_within_image(clock_tower_location):
            time.sleep(1)
            if (clocktower_boost_btn_location := check_image_presence(clocktower_boost_btn, confidence=0.8)):
                click_random_within_image(clocktower_boost_btn_location)
                time.sleep(1)
                if (clocktower_boost_btn2_location := check_image_presence(clocktower_boost_btn2, confidence=0.8)):
                    click_random_within_image(clocktower_boost_btn2_location)
                    time.sleep(1)
                    setlog("Boosted clock tower", "success")
                    do_click(905, 283) # click away
                    return True
                else:
                    setlog("Error: Boost button not found!", 'error')
                    return False
            else:
                setlog("Error: Free Boost button not found!", 'error')
                return False
    else:
        setlog("No clock tower boost icon found", "warning")
        return False

def bb_collect_resource(assets_path):
    bb_gold = assets_path + '\\bb_assets\\bb_gold.png'
    bb_elixir = assets_path + '\\bb_assets\\bb_elixir.png'
    bb_gem = assets_path + '\\bb_assets\\bb_gem.png'

    resources_imges = [bb_gold, bb_elixir, bb_gem]
    random.shuffle(resources_imges)
    collected_resources = False

    for resource_img in resources_imges:
        if (resource_location := check_image_presence(resource_img, confidence=0.8)):
            try:
                click_random_within_image(resource_location)
            except pyautogui.ImageNotFoundException:
                setlog(f"Image: {resource_img} not found", "info")
            resource_name = resource_img.split('\\')[-1].split('.')[0].capitalize()
            setlog(f"Collected {resource_name}", "success")
            collected_resources = True

    if collected_resources:
        setlog("Resources collected", "info")
    else:
        setlog("No resources collected", "info")

    return collected_resources

def collect_clan_capital_gold(assets_path):
    clan_capital_gold_img = assets_path + '\\mv_assets\\clan_capital_gold.png'
    cc_collect_btn_img = assets_path + '\\mv_assets\\cc_collect_btn.png'

    scroll_to_zoom((716, 117), 10)
    click_drag(470, 316, 725, 82)
    time.sleep(2)
    if (clan_capital_gold_location := check_image_presence(clan_capital_gold_img, confidence=0.8)):
        click_random_within_image(clan_capital_gold_location)
        time.sleep(1)
        if (cc_collect_btn_location := check_image_presence(cc_collect_btn_img, confidence=0.8)):
            click_random_within_image(cc_collect_btn_location)
            time.sleep(1)
            setlog("Collected clan capital gold", "success")
            return True
        else:
            setlog("Collect button not found", "error")
            return False
    else:
        setlog("Clan capital gold not found", "warning")
        return False

def collect_gem_box(assets_path):
    gem_box_img = assets_path + '\\mv_assets\\gem_box.png'
    if (gem_box_location := check_image_presence(gem_box_img, confidence=0.8)):
        click_random_within_image(gem_box_location)
        time.sleep(1)
        do_click(467, 449)
        setlog("Collected gem box", "success")
        do_click(905, 283) # click away
        do_click(905, 283) # click away
        return True
    else:
        setlog("Gem box not found", "warning")
        return False

def collect_loop(skip_scc_num=0):
    count = 0
    while 1:

        count += 1
        if skip_scc_num == count:
            count += 1

        switch_acc(assets_path, acc_num=count)

        if count >= 21:
            count = 0
            setlog("max accounts reached", "info")
            setlog("Resetting counter", "info")

        is_army_btn_visible()
        scroll_to_zoom((716, 117), 10)
        collect_resources(assets_path)
        collect_gem_box(assets_path)
        collect_clan_capital_gold(assets_path)
        collect_gem_box(assets_path)
        time.sleep(1)

        if go_to_bb():
            bb_collect_resource(assets_path)
            boost_clock_tower(assets_path)
            go_to_bb(True) # go back to main village

if __name__ == "__main__":

    collect_loop(skip_scc_num=1)
