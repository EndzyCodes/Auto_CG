import pyautogui
import time

if __name__ == "__main__":
    img = r'C:\Users\Mark\Documents\GitHub\EndzyCodes\Auto_CG\assets\test\anniv_cake.png'

    locations = []
    try:
        for loc in pyautogui.locateAllOnScreen(img, confidence=0.6):
            print(f"Found at: {loc}")
            
            # pyautogui.alert(text=loc, title='WARNING', button='OK')
            locations.append(loc)

        if locations:
            for loc in locations:
                pyautogui.moveTo(loc.left, loc.top)
                time.sleep(1)
        else:
            print("Not Found")
    except Exception as e:
        print(f"An error occurred: {e}")