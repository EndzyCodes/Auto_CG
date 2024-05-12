import json
from Functions import setlog, get_coc_window, set_window_size, launch_coc, window_title
from cg_funcs import cg_mode_loop
from bb_funcs import bb_attack_loop
from mv_funcs import main_village_attack_loop
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QCheckBox, QPushButton, QGroupBox, QTabWidget, QRadioButton, QToolTip, QSplashScreen, QLabel
from PyQt6.QtCore import QThread, pyqtSignal, Qt, QTimer, QRect
from PyQt6.QtGui import QPixmap
import sys
import time

# def main(attack_only_no_cg=False,
#         enable_gem_cooldown=False,
#         clan_games_mode=False):

#     bb_attack_loop(attack_only_no_cg=attack_only_no_cg, clan_games_mode=clan_games_mode, gem_cooldown=enable_gem_cooldown)

def main(clan_games_mode, BB_atk_only_mode, 
        MV_atk_only_mode, switch_accounts, 
        solo_account, BBcollect_resources, 
        BBactivate_CT_boost, BBsecond_camp, 
        gem_cooldown
        ):

    if get_coc_window(window_title):
        pass
    else:
        launch_coc()

    set_window_size(window_name="coc")
    setlog("Starting automated gameplay...", 'info')
    # Example: Implement automation logic
    while True:
        if clan_games_mode:
            setlog("---- Clan Games Mode ----", "info")
            cg_mode_loop(gem_cooldown=gem_cooldown)
            pass
        elif BB_atk_only_mode:
            setlog("---- BB Attack Only Mode ----", "info")
            print(BBsecond_camp)
            bb_attack_loop(isSwitchAcc=switch_accounts, is_2_camps=BBsecond_camp)
        elif MV_atk_only_mode:
            setlog("---- Main Village Attack Only Mode ----", "info")
            main_village_attack_loop(isSwitchAcc=switch_accounts)
            pass
        else:
            setlog("No mode selected", "warning")

class TabBase(QWidget): # template for when we need to create a new tab just copy paste this then change the class name
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # Implement setup for each tab (to be overridden by subclasses)
        pass

    def loadSettings(self, settings):
        # Load settings for each tab (to be overridden by subclasses)
        pass

    def saveSettings(self, settings):
        # Save settings for each tab (to be overridden by subclasses)
        pass

class MiscTab(QWidget):
    def initUI(self):
        # Implement setup for the Miscellaneous tab
        modes_group_box = QGroupBox("Modes", self)
        modes_group_box.setGeometry(10, 10, 200, 110)

        self.CGmode_rd = QRadioButton("Clan Games Mode", modes_group_box)
        self.CGmode_rd.move(10, 20)
        self.CGmode_rd.setToolTip('Clan Games and BB attack to complete challenges.')

        self.BBAtkOnlymode_rd = QRadioButton("BB Attack Only", modes_group_box)
        self.BBAtkOnlymode_rd.move(10, 40)
        self.BBAtkOnlymode_rd.setToolTip('BB attack only, no main village attacks or Clan Games.')

        self.MVatkOnlymode_rd = QRadioButton("MV Attack Only", modes_group_box)
        self.MVatkOnlymode_rd.move(10, 60)
        self.MVatkOnlymode_rd.setToolTip('Main Village attack only, no BB attacks or Clan Games.')

        self.DonateOnlymode_rd = QRadioButton("Donate Only mode", modes_group_box)
        self.DonateOnlymode_rd.move(10, 80)
        self.DonateOnlymode_rd.setToolTip('Donate troops on current acc, switches acc if no more req then goes back to the selected acc for donation')


        SA_modes_group_box = QGroupBox("Switch Account Settings", self)
        SA_modes_group_box.setGeometry(225, 10, 200, 100)

        self.SwitchAccts_rd = QRadioButton("Switch accounts", SA_modes_group_box)
        self.SwitchAccts_rd.move(10, 20)
        self.SwitchAccts_rd.setToolTip('Enable account switching.')

        self.SoloAcc_rd = QRadioButton("Solo account", SA_modes_group_box)
        self.SoloAcc_rd.move(10, 40)
        self.SoloAcc_rd.setToolTip('Only use one account.')

    def loadSettings(self, settings):
        self.CGmode_rd.setChecked(settings.get("clanGamesMode", False))
        self.BBAtkOnlymode_rd.setChecked(settings.get("BBattackOnlyMode", False))
        self.MVatkOnlymode_rd.setChecked(settings.get("MVattackOnlyMode", False))
        self.DonateOnlymode_rd.setChecked(settings.get("donateOnlyMode", False))
        self.SwitchAccts_rd.setChecked(settings.get("switchAccounts", False))
        self.SoloAcc_rd.setChecked(settings.get("soloAccount", False))

    def saveSettings(self, settings):
        settings["clanGamesMode"] = self.CGmode_rd.isChecked()
        settings["BBattackOnlyMode"] = self.BBAtkOnlymode_rd.isChecked()
        settings["MVattackOnlyMode"] = self.MVatkOnlymode_rd.isChecked()
        settings["donateOnlyMode"] = self.DonateOnlymode_rd.isChecked()
        settings["switchAccounts"] = self.SwitchAccts_rd.isChecked()
        settings["soloAccount"] = self.SoloAcc_rd.isChecked()

class BuilderBaseTab(QWidget):
    def initUI(self):
        # Implement setup for the Builder Base tab
        self.BBsettings_group_box = QGroupBox("Collect and Activate", self)
        self.BBsettings_group_box.setGeometry(10, 10, 200, 100)

        self.BBChkCollectResources = QCheckBox("Collect Resources", self.BBsettings_group_box)
        self.BBChkCollectResources.move(10, 20)
        self.BBChkCollectResources.setToolTip('Collect resources in Builder Base.')

        self.BBChkActivateCTBoost = QCheckBox("Activate Clocktower Boost", self.BBsettings_group_box)
        self.BBChkActivateCTBoost.move(10, 40)
        self.BBChkActivateCTBoost.setToolTip('Activate Clocktower boost in Builder Base.')

        BBarmy_config_group_box = QGroupBox("BB Army Configuration", self)
        BBarmy_config_group_box.setGeometry(225, 10, 200, 100)

        self.BBsecondCamp = QCheckBox("2nd camp", BBarmy_config_group_box)
        self.BBsecondCamp.move(10, 20)
        self.BBsecondCamp.setToolTip('Enable this if the account has 2 reinforcement camps, 1st one for loons, 2nd one for minions.')

    def loadSettings(self, settings):
        self.BBChkCollectResources.setChecked(settings.get("BBCollectResources", False))
        self.BBChkActivateCTBoost.setChecked(settings.get("BBActivateCTBoost", False))
        self.BBsecondCamp.setChecked(settings.get("BBsecondCamp", False))

    def saveSettings(self, settings):
        settings["BBCollectResources"] = self.BBChkCollectResources.isChecked()
        settings["BBActivateCTBoost"] = self.BBChkActivateCTBoost.isChecked()
        settings["BBsecondCamp"] = self.BBsecondCamp.isChecked()

class MainVillageTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # Implement setup for each tab (to be overridden by subclasses)
        pass

    def loadSettings(self, settings):
        # Load settings for each tab (to be overridden by subclasses)
        pass

    def saveSettings(self, settings):
        # Save settings for each tab (to be overridden by subclasses)
        pass

class ClanGamesTab(QWidget):
    def initUI(self):
        # Implement setup for the Clan Games tab
        self.CGsettings_group_box = QGroupBox("Clan Games Settings", self)
        self.CGsettings_group_box.setGeometry(15, 10, 200, 100)

        self.gemCooldownCheckbox = QCheckBox("Gem Challenge Cooldown", self.CGsettings_group_box)
        self.gemCooldownCheckbox.move(10, 20)
        self.gemCooldownCheckbox.setToolTip('Spend gems to speed up a challenge purge.')

    def loadSettings(self, settings):
        self.gemCooldownCheckbox.setChecked(settings.get("gemCooldown", False))

    def saveSettings(self, settings):
        settings["gemCooldown"] = self.gemCooldownCheckbox.isChecked()

class CustomSplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Custom Splash Screen')
        self.setFixedSize(800, 300)  # Set the size of the splash screen widget

        # Create a layout for the splash screen
        layout = QVBoxLayout(self)

        # Load and display the splash screen image
        pixmap = QPixmap('C:/Users/Mark/Documents/GitHub/EndzyCodes/Auto_CG/assets/coc_loading_Screen.png')
        splash_image = QLabel(self)
        splash_image.setPixmap(pixmap)
        layout.addWidget(splash_image, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add a loading message
        loading_label = QLabel('Loading...', self)  # Create the loading label here
        loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(loading_label)

        # Timer to close the splash screen after a delay (e.g., 2 seconds)
        QTimer.singleShot(2000, self.close)


class ClashOfClansBotGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        # Show splash screen
        splash = CustomSplashScreen()
        splash.show()
        time.sleep(2)

        self.initUI()
        # self.settings = {"clanGamesMode": False, # Misc Settings
        #                 "BBattackOnlyMode": False,
        #                 "BBCollectResources": False, # Builder base settings
        #                 "BBActivateCTBoost": False,
        #                 "gemCooldown": False # Clan Games settings
        #                 }
        self.loadSettings()
        set_window_size(window_name="terminal") # set terminal size for bot
        self.bot_thread = None

        # Close splash screen after main window is shown
        splash.close()

    def initUI(self):
        self.setWindowTitle('Clash Buddy v1.0')
        self.setFixedSize(452, 550) # Set the fixed size of the window (width, height)
        # this is the main window
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setGeometry(7, 10, 440, 470) # x, y, width, height of the tabs
        # self.tab_widget.currentChanged.connect(self.tabChanged)  # Connect tab change event

        # Create and add tabs
        self.misc_tab = MiscTab()
        self.bb_attack_tab = BuilderBaseTab()
        self.main_village_tab = MainVillageTab()
        self.clan_games_tab = ClanGamesTab()

        # * create the tabs here
        self.tab_widget.addTab(self.misc_tab, "Misc")
        self.tab_widget.addTab(self.bb_attack_tab, "Builder Base")
        self.tab_widget.addTab(self.main_village_tab, "Main Village")
        self.tab_widget.addTab(self.clan_games_tab, "Clan Games")

        # * Setup specific tab UIs and connect events if needed
        self.misc_tab.initUI()
        self.bb_attack_tab.initUI()
        self.main_village_tab.initUI()
        self.clan_games_tab.initUI()

        self.setupBottomButtons()
        self.move(560, 35) # move GUI window  beside the google play games emulator

    def setupBottomButtons(self):
        y_pos = 490
        # * Add buttons to bottom
        self.saveSettingsButton = QPushButton("Save Settings", self)
        self.saveSettingsButton.move(310, y_pos)
        self.saveSettingsButton.resize(120, 40)
        self.saveSettingsButton.clicked.connect(self.saveSettings)

        self.startButton = QPushButton("Start Bot", self)
        self.startButton.move(30, y_pos)
        self.startButton.resize(120, 40)
        self.startButton.clicked.connect(self.startBot)  # Connect the button to startBot method

        self.stopButton = QPushButton("Stop Bot", self)
        self.stopButton.move(170, y_pos)
        self.stopButton.resize(120, 40)
        self.stopButton.clicked.connect(self.stopBot)  # Connect the button to stopBot method

    def loadSettings(self):
        try:
            with open("settings.json", "r") as file:
                self.settings = json.load(file)
                setlog(f"Settings loaded successfully: {self.settings}", 'success')
                # * load settings into tabs
                self.misc_tab.loadSettings(self.settings)
                self.bb_attack_tab.loadSettings(self.settings)
                self.main_village_tab.loadSettings(self.settings)
                self.clan_games_tab.loadSettings(self.settings)
        except FileNotFoundError:
            setlog("Settings file not found. Using default settings.", 'error')
            # If settings file is not found, initialize with default settings
            self.settings = {
                "clanGamesMode": False,
                "BBattackOnlyMode": False,
                "MVattackOnlyMode": False,
                "BBCollectResources": False,
                "BBActivateCTBoost": False,
                "BBsecondCamp": False,
                "gemCooldown": False
            }
        except json.JSONDecodeError:
            setlog("Error loading settings file. Using default settings.", 'error')
            # If error decoding settings file, initialize with default settings
            self.settings = {
                "clanGamesMode": False,
                "BBattackOnlyMode": False,
                "MVattackOnlyMode": False,
                "BBCollectResources": False,
                "BBActivateCTBoost": False,
                "BBsecondCamp": False,
                "gemCooldown": False
            }

    def saveSettings(self):
        try:
            # * Save settings for each tab
            self.misc_tab.saveSettings(self.settings)
            self.bb_attack_tab.saveSettings(self.settings)
            self.main_village_tab.saveSettings(self.settings)
            self.clan_games_tab.saveSettings(self.settings)

            with open("settings.json", "w") as file:
                json.dump(self.settings, file)
            setlog("Settings saved successfully.", 'success')
        except Exception as e:
            setlog(f"Error saving settings: {e}", 'error')

    def startBot(self):
        # * Set variables boolean value based on checkboxes state, it a checkbox is checked, it will be True, otherwise False
        self.saveSettings()  # Save settings when starting the bot
        # Misc tab
        clan_games_mode = self.settings["clanGamesMode"]
        bb_atk_only_mode = self.settings["BBattackOnlyMode"]
        mv_atk_only_mode = self.settings["MVattackOnlyMode"]
        switch_accounts = self.settings["switchAccounts"]
        solo_account = self.settings["soloAccount"]
        # BB tab
        BBcollect_resources = self.settings["BBCollectResources"]
        BBactivate_CT_boost = self.settings["BBActivateCTBoost"]
        is_2_camps = self.settings["BBsecondCamp"]
        # CG tab
        enable_gem_cooldown = self.settings["gemCooldown"]

        print(
            f"Starting bot with configurations: "
            f"Clan Games Mode: {clan_games_mode}, "
            f"BB Attack Only Mode: {bb_atk_only_mode}, "
            f"MV Attack Only Mode: {mv_atk_only_mode}, "
            f"Switch Accounts: {switch_accounts}, "
            f"Solo Account: {solo_account}, "
            f"BB Collect Resources: {BBcollect_resources}, "
            f"BB Activate CT Boost: {BBactivate_CT_boost},"
            f"BB Second Camp: {is_2_camps}, "
            f"Gem Cooldown: {enable_gem_cooldown}"
        )

        # If there's an existing thread, wait for it to finish before creating a new one
        if self.bot_thread and self.bot_thread.isRunning():
            print("Waiting for the previous bot thread to finish...")
            self.bot_thread.wait()

        # * pass the variables to the functions that need them
        # Create a new thread to run the bot
        self.bot_thread = BotThread(
            clan_games_mode,
            bb_atk_only_mode,
            mv_atk_only_mode,
            switch_accounts,
            solo_account,
            BBcollect_resources,
            BBactivate_CT_boost,
            is_2_camps,
            enable_gem_cooldown,
        )

        self.bot_thread.finished.connect(self.onBotThreadFinished)
        self.bot_thread.start()

    def stopBot(self):
        if self.bot_thread and self.bot_thread.isRunning():
            setlog("Stopping bot...", "warning")
            self.bot_thread.terminate()  # Terminate the bot thread if it's running

    def onBotThreadFinished(self):
        setlog("Bot thread finished.", "success")
        self.bot_thread = None  # Reset the thread reference

    def keyPressEvent(self, event):
        '''
            Overriding the key press event to handle Ctrl+X shortcut to close window
        '''
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_X:
            set_window_size(window_name="terminal", noramal_size=True) # Reset terminal size
            self.close()

class BotThread(QThread):
    def __init__(self, clan_games_mode,  
                BB_atk_only_mode, 
                MV_atk_only_mode,
                switch_accounts,
                solo_account,
                BBcollect_resources,
                BBactivate_CT_boost,
                BBsecond_camp,
                gem_cooldown):

        super().__init__()
        # Misc tab variables
        self.clan_games_mode = clan_games_mode
        self.bb_atk_only_mode = BB_atk_only_mode
        self.mv_atk_only_mode = MV_atk_only_mode
        self.switch_accounts = switch_accounts
        self.solo_account = solo_account
        # BB tab variables
        self.BBcollect_resources = BBcollect_resources
        self.BBactivate_CT_boost = BBactivate_CT_boost
        self.BBsecond_camp = BBsecond_camp
        # CG tab variables
        self.gem_cooldown = gem_cooldown

    def run(self):
        # Call your main bot function from here
        main(clan_games_mode = self.clan_games_mode, 
            BB_atk_only_mode = self.bb_atk_only_mode, 
            MV_atk_only_mode = self.mv_atk_only_mode,
            switch_accounts = self.switch_accounts,
            solo_account = self.solo_account,

            BBcollect_resources = self.BBcollect_resources,
            BBactivate_CT_boost = self.BBactivate_CT_boost,
            BBsecond_camp = self.BBsecond_camp,

            gem_cooldown = self.gem_cooldown)
