import json
from Functions import setlog, get_coc_window, window_title
from bb_funcs import bb_attack_loop
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QPushButton, QGroupBox, QTabWidget, QRadioButton, QToolTip
from PyQt6.QtCore import QThread, pyqtSignal, Qt, QTimer

# def main(attack_only_no_cg=False,
#         enable_gem_cooldown=False,
#         clan_games_mode=False):

#     bb_attack_loop(attack_only_no_cg=attack_only_no_cg, clan_games_mode=clan_games_mode, gem_cooldown=enable_gem_cooldown)

def main(gem_cooldown,
        clan_games_mode,
        attack_only_no_cg,
        ):

    get_coc_window(window_title)

    print("Starting automated gameplay...")
    # Example: Implement automation logic
    while True:
        bb_attack_loop(attack_only_no_cg=attack_only_no_cg,
                        clan_games_mode=clan_games_mode,
                        gem_cooldown=gem_cooldown)

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

class MiscTab(TabBase):
    def initUI(self):
        # Implement setup for the Miscellaneous tab
        modes_group_box = QGroupBox("Modes", self)
        modes_group_box.setGeometry(15, 10, 200, 100)

        self.CGmode_rd = QRadioButton("Clan Games Mode", modes_group_box)
        self.CGmode_rd.move(10, 20)
        self.CGmode_rd.setToolTip('Clan Games and BB attack to complete challenges.')

        self.BBAtkOnlymode_rd = QRadioButton("BB Attack Only", modes_group_box)
        self.BBAtkOnlymode_rd.move(10, 40)
        self.BBAtkOnlymode_rd.setToolTip('BB attack only, no main village attacks or clan games.')

        SA_modes_group_box = QGroupBox("Switch Account Settings", self)
        SA_modes_group_box.setGeometry(240, 10, 200, 100)

        self.SwitchAccts_rd = QRadioButton("Switch accounts", SA_modes_group_box)
        self.SwitchAccts_rd.move(10, 20)
        self.SwitchAccts_rd.setToolTip('Enable account switching.')

        self.SoloAcc_rd = QRadioButton("Solo account", SA_modes_group_box)
        self.SoloAcc_rd.move(10, 40)
        self.SoloAcc_rd.setToolTip('Only use one account.')

    def loadSettings(self, settings):
        self.CGmode_rd.setChecked(settings.get("clanGamesMode", False))
        self.BBAtkOnlymode_rd.setChecked(settings.get("BBattackOnlyMode", False))
        self.SwitchAccts_rd.setChecked(settings.get("switchAccounts", False))
        self.SoloAcc_rd.setChecked(settings.get("soloAccount", False))

    def saveSettings(self, settings):
        settings["BBattackOnlyMode"] = self.BBAtkOnlymode_rd.isChecked()
        settings["clanGamesMode"] = self.CGmode_rd.isChecked()
        settings["switchAccounts"] = self.SwitchAccts_rd.isChecked()
        settings["soloAccount"] = self.SoloAcc_rd.isChecked()

class BuilderBaseTab(TabBase):
    def initUI(self):
        # Implement setup for the Builder Base tab
        self.BBsettings_group_box = QGroupBox("Collect & Activate", self)
        self.BBsettings_group_box.setGeometry(15, 15, 200, 100)

        self.BBChkCollectResources = QCheckBox("Collect Resources", self.BBsettings_group_box)
        self.BBChkCollectResources.move(10, 20)
        self.BBChkCollectResources.setToolTip('Collect resources in Builder Base.')

        self.BBChkActivateCTBoost = QCheckBox("Activate Clocktower Boost", self.BBsettings_group_box)
        self.BBChkActivateCTBoost.move(10, 40)
        self.BBChkActivateCTBoost.setToolTip('Activate Clocktower boost in Builder Base.')

    def loadSettings(self, settings):
        self.BBChkCollectResources.setChecked(settings.get("BBCollectResources", False))
        self.BBChkActivateCTBoost.setChecked(settings.get("BBActivateCTBoost", False))

    def saveSettings(self, settings):
        settings["BBCollectResources"] = self.BBChkCollectResources.isChecked()
        settings["BBActivateCTBoost"] = self.BBChkActivateCTBoost.isChecked()

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

class ClanGamesTab(TabBase):
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

class ClashOfClansBotGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        # self.settings = {"clanGamesMode": False, # Misc Settings
        #                 "BBattackOnlyMode": False, 
        #                 "BBCollectResources": False, # Builder base settings
        #                 "BBActivateCTBoost": False,
        #                 "gemCooldown": False # Clan Games settings
        #                 }
        self.loadSettings()
        self.bot_thread = None

    def initUI(self):
        self.setWindowTitle('Clash of Clans Bot Configuration')
        self.setFixedSize(480, 550) # Set the fixed size of the window (width, height)
        # this is the main window
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setGeometry(10, 10, 465, 470) # x, y, width, height of the tabs
        # self.tab_widget.currentChanged.connect(self.tabChanged)  # Connect tab change event

        # Create and add tabs
        self.misc_tab = MiscTab()
        self.bb_attack_tab = BuilderBaseTab()
        self.main_village_tab = MainVillageTab()
        self.clan_games_tab = ClanGamesTab()

        #* create the tabs here
        self.tab_widget.addTab(self.misc_tab, "Misc")
        self.tab_widget.addTab(self.bb_attack_tab, "Builder Base")
        self.tab_widget.addTab(self.main_village_tab, "Main Village")
        self.tab_widget.addTab(self.clan_games_tab, "Clan Games")

        #* Setup specific tab UIs and connect events if needed
        self.misc_tab.initUI()
        self.bb_attack_tab.initUI()
        self.main_village_tab.initUI()
        self.clan_games_tab.initUI()

        self.setupBottomButtons()

    def setupBottomButtons(self):
        y_pos = 490
        #* Add buttons to bottom
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
                #* load settings into tabs
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
                "BBCollectResources": False,
                "BBActivateCTBoost": False,
                "gemCooldown": False
            }
        except json.JSONDecodeError:
            setlog("Error loading settings file. Using default settings.", 'error')
            # If error decoding settings file, initialize with default settings
            self.settings = {
                "clanGamesMode": False,
                "BBattackOnlyMode": False,
                "BBCollectResources": False,
                "BBActivateCTBoost": False,
                "gemCooldown": False
            }

    def saveSettings(self):
        try:
            #* Save settings for each tab
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
        #* Set variables boolean value based on checkboxes state, it a checkbox is checked, it will be True, otherwise False
        self.saveSettings()  # Save settings when starting the bot
        clan_games_mode = self.settings["clanGamesMode"]
        attack_only_no_cg = self.settings["BBattackOnlyMode"]
        enable_gem_cooldown = self.settings["gemCooldown"]

        print(f"Starting bot with configurations: "
                f"Clan Games Mode: {clan_games_mode}, "
                f"BB Attack Only Mode: {attack_only_no_cg}, "
                f"Gem Cooldown: {enable_gem_cooldown}")

        # If there's an existing thread, wait for it to finish before creating a new one
        if self.bot_thread and self.bot_thread.isRunning():
            print("Waiting for the previous bot thread to finish...")
            self.bot_thread.wait()

        #* pass the variables to the functions that need them

        # Create a new thread to run the bot
        self.bot_thread = BotThread(enable_gem_cooldown, clan_games_mode, attack_only_no_cg)
        self.bot_thread.finished.connect(self.onBotThreadFinished)
        self.bot_thread.start()

    def stopBot(self):
        if self.bot_thread and self.bot_thread.isRunning():
            setlog("Stopping bot...", "warning")
            self.bot_thread.terminate()  # Terminate the bot thread if it's running

    def onBotThreadFinished(self):
        setlog("Bot thread finished.", "success")
        self.bot_thread = None  # Reset the thread reference

class BotThread(QThread):
    def __init__(self, gem_cooldown, clan_games_mode, attack_only_no_cg):
        super().__init__()
        self.gem_cooldown = gem_cooldown
        self.clan_games_mode = clan_games_mode
        self.attack_only_no_cg = attack_only_no_cg

    def run(self):
        # Call your main bot function from here
        main(attack_only_no_cg=self.attack_only_no_cg, clan_games_mode=self.clan_games_mode, gem_cooldown=self.gem_cooldown)