import time
from ...Functions.image_detection import check_image_presence, click_random_within_image
from ...Functions.click_utils import do_click
from ...Functions.logging_utils import setlog

def request_troops():

    region_trash_btn = (421, 355, 105, 43)

    trash_btn_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\donate_assets\trash_btn.png'
    ok_btn_img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\donate_assets\ok_btn.png'

    if (trash_btn_location := check_image_presence(trash_btn_img, region=region_trash_btn)):
        setlog("Found troops in cc, removing troops now")
        click_random_within_image(trash_btn_location)
        time.sleep(1)
        if (ok_btn_location := check_image_presence(ok_btn_img)):
            click_random_within_image(ok_btn_location)
            do_click(734, 467) # click request button
            time.sleep(1)
            do_click(551, 402) # click send button
            setlog("Troop request successfully sent!", 'info')
    else:
        setlog("No troops in cc, skip click trash", 'info')
        do_click(734, 467) # click request button
        time.sleep(1)
        do_click(551, 402) # click send button
        setlog("Troop request successfully sent!", 'info')
