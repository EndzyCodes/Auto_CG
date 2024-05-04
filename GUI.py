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

class ClashOfClansBotGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.settings = {"clanGamesMode": False, # Misc Settings
                        "BBattackOnlyMode": False, 
                        "BBCollectResources": False, # Builder base settings
                        "BBActivateCTBoost": False,
                        "gemCooldown": False # Clan Games settings
                        }
        self.loadSettings()
        self.bot_thread = None

    def initUI(self):
        self.setWindowTitle('Clash of Clans Bot Configuration')
        self.setFixedSize(480, 550) # Set the fixed size of the window (width, height)
        # this is the main window
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setGeometry(10, 10, 465, 470) # x, y, width, height of the tabs
        # self.tab_widget.currentChanged.connect(self.tabChanged)  # Connect tab change event

        #* Create the widgets for each tab here
        self.misc_tab = QWidget()
        self.bb_attack_tab = QWidget()
        self.main_village_tab = QWidget()
        self.clan_games_tab = QWidget()

        #* create the tabs here
        self.tab_widget.addTab(self.misc_tab, "Misc")
        self.tab_widget.addTab(self.bb_attack_tab, "Builder Base")
        self.tab_widget.addTab(self.main_village_tab, "Main Village")
        self.tab_widget.addTab(self.clan_games_tab, "Clan Games")

        #* call the tab functions here
        self.setupMiscTab()
        self.setupBuilderBaseTab()
        self.setupClanGamesTab()
        self.setupBottomButtons()

        #* Set tooltips here
        # Clan games tab
        # self.gemCooldownCheckbox.setToolTip('Spend gems to speed up a challenge purge.')
        # self.CGmode_rd.setToolTip('Clan Games and BB attack to complete challenges.')
        # self.BBAtkOnlymode_rd.setToolTip('BB attack only, no main village attacks or clan games.')
        # Builder Base tab
        # self.BBChkCollectResources.setToolTip('Collect resources in Builder Base.')
        # self.BBChkActivateCTBoost.setToolTip('Activate Clocktower boost in Builder Base.')

        #* Connect hover events to show tooltips after a delay
        # Clan games tab
        # self.connectHoverEvents(self.gemCooldownCheckbox)
        # self.connectHoverEvents(self.CGmode_rd)
        # self.connectHoverEvents(self.BBAtkOnlymode_rd)
        # # Builder Base  tab
        # self.connectHoverEvents(self.BBChkCollectResources)
        # self.connectHoverEvents(self.BBChkActivateCTBoost)

    def connectHoverEvents(self, widget):
        # Create a timer to trigger the tooltip
        hoverTimer = QTimer(self)
        hoverTimer.setSingleShot(True)
        hoverTimer.timeout.connect(lambda: QToolTip.showText(widget.mapToGlobal(widget.rect().center()), widget.toolTip()))

        # Connect hover events
        widget.enterEvent = lambda event: hoverTimer.start(1000)  # Start timer after 1 second
        widget.leaveEvent = lambda event: hoverTimer.stop()       # Stop timer on mouse leave

    def tabChanged(self, index): #TODO - need to fix this
        if index == 0:  # Clan Games Tab
            self.setupClanGamesTab()
            self.setupBuilderBaseTab() #TODO - this is the hint, it only shows the gui on other tabs if its called on index 0
            # self.CGTab_setupModesGroupBox()
        elif index == 1:  # BB Attack Tab
            self.setupBuilderBaseTab()
        elif index == 2:  # Main Village Tab
            self.setupMainVillageTab()
        # else:
        #     self.removeClanGamesTabWidgets()
            #  later add here for other tabs

    def setupMiscTab(self): # Miscellaneous tab
        #* Modes group box
        modes_group_box = QGroupBox("Modes", self.misc_tab)
        modes_group_box.setGeometry(15, 10, 200, 100)
        # rd = radio, chk = check box
        # Modes options
        self.CGmode_rd = QRadioButton("Clan Games Mode", modes_group_box)
        self.CGmode_rd.move(10, 20)
        self.CGmode_rd.setToolTip('Clan Games and BB attack to complete challenges.')

        self.BBAtkOnlymode_rd = QRadioButton("BB Attack Only", modes_group_box)
        self.BBAtkOnlymode_rd.move(10, 40)
        self.BBAtkOnlymode_rd.setToolTip('BB attack only, no main village attacks or clan games.')

        #* Switch acc group box
        SA_modes_group_box = QGroupBox("Switch Account Settings", self.misc_tab)
        SA_modes_group_box.setGeometry(240, 10, 200, 100)

        # Switch acc options
        self.SwitchAccts_rd = QRadioButton("Switch accounts", SA_modes_group_box)
        self.SwitchAccts_rd.move(10, 20)
        self.SwitchAccts_rd.setToolTip('Enable account switching.')

        self.SoloAcc_rd = QRadioButton("Solo account", SA_modes_group_box)
        self.SoloAcc_rd.move(10, 40)
        self.SoloAcc_rd.setToolTip('Only use one account.')

    def setupClanGamesTab(self):
        # self.removeClanGamesTabWidgets()  # Clear previous widgets if any
        #* Clan Games Settings group box
        self.CGsettings_group_box = QGroupBox("Clan Games Settings", self.clan_games_tab)
        self.CGsettings_group_box.setGeometry(15, 10, 200, 100)

        self.gemCooldownCheckbox = QCheckBox("Gem Challenge Cooldown", self.CGsettings_group_box)
        self.gemCooldownCheckbox.move(10, 20)
        self.gemCooldownCheckbox.setToolTip('Spend gems to speed up a challenge purge.')

    def removeClanGamesTabWidgets(self):
        # if hasattr(self, 'CGsettings_group_box'):
        self.CGsettings_group_box.setParent(None)
        self.CGsettings_group_box.deleteLater()
        #* delete the widgets here
        del self.gemCooldownCheckbox

        del self.CGmode_rd
        del self.BBAtkOnlymode_rd

    def setupBuilderBaseTab(self):
        bb_attack_tab = QWidget()
        bb_attack_layout = QVBoxLayout()
        bb_attack_tab.setLayout(bb_attack_layout)

        self.BBsettings_group_box = QGroupBox("Collect & Activate", self.bb_attack_tab)
        self.BBsettings_group_box.setGeometry(15, 15, 200, 100)

        self.BBChkCollectResources = QCheckBox("Collect Resources", self.BBsettings_group_box)
        self.BBChkCollectResources.move(10, 20)
        self.BBChkCollectResources.setToolTip('Collect resources in Builder Base.')

        self.BBChkActivateCTBoost = QCheckBox("Activate Clocktower Boost", self.BBsettings_group_box)
        self.BBChkActivateCTBoost.move(10, 40)
        self.BBChkActivateCTBoost.setToolTip('Activate Clocktower boost in Builder Base.')

    def setupMainVillageTab(self):
        main_village_tab = QWidget()
        main_village_layout = QVBoxLayout()
        main_village_tab.setLayout(main_village_layout)

        # Add Main Village tab content here...

        # self.tab_widget.addTab(main_village_tab, "Main Village")

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
        setlog("Loading settings...", 'info')
        try:
            with open("settings.json", "r") as file:
                self.settings = json.load(file)
                setlog(f"Settings loaded successfully: {self.settings}", 'success')
                #* Set checkbox states based on loaded settings
                #* Misc tab
                self.CGmode_rd.setChecked(self.settings.get("clanGamesMode", False))
                self.BBAtkOnlymode_rd.setChecked(self.settings.get("BBattackOnlyMode", False))
                self.SwitchAccts_rd.setChecked(self.settings.get("switchAccounts", False))
                self.SoloAcc_rd.setChecked(self.settings.get("soloAccount", False))
                #* Builder Base tab
                self.BBChkCollectResources.setChecked(self.settings.get("BBCollectResources", False))
                self.BBChkActivateCTBoost.setChecked(self.settings.get("BBActivateCTBoost", False))
                #* Clan games tab
                self.gemCooldownCheckbox.setChecked(self.settings.get("gemCooldown", False))

        except FileNotFoundError:
            setlog("Settings file not found. Using default settings.", 'error')
        except json.JSONDecodeError:
            setlog("Error loading settings file. Using default settings.", 'error')

    def saveSettings(self):
        try:
            #* Misc tab
            self.settings["BBattackOnlyMode"] = self.BBAtkOnlymode_rd.isChecked()
            self.settings["clanGamesMode"] = self.CGmode_rd.isChecked()

            #* Builder Base tab
            self.settings["BBCollectResources"] = self.BBChkCollectResources.isChecked()
            self.settings["BBActivateCTBoost"] = self.BBChkActivateCTBoost.isChecked()

            #* Clan Games tab
            self.settings["gemCooldown"] = self.gemCooldownCheckbox.isChecked()

            with open("settings.json", "w") as file:
                json.dump(self.settings, file)
            setlog("Settings saved successfully.", 'success')
        except Exception as e:
            setlog(f"Error saving settings: {e}", 'error')

    def startBot(self):
        #* Set variables boolean value based on checkboxes state, it a checkbox is checked, it will be True, otherwise False
        clan_games_mode = self.CGmode_rd.isChecked()
        attack_only_no_cg = self.BBAtkOnlymode_rd.isChecked()
        enable_gem_cooldown = self.gemCooldownCheckbox.isChecked()
        self.saveSettings()  # Save settings when starting the bot

        print(f"Starting bot with configurations: "
            f"Clan Games Mode: {self.settings['clanGamesMode']}, "
            f"BB Attack Only Mode: {self.settings['BBattackOnlyMode']}, "
            f"Switch Accounts: {self.settings['switchAccounts']}, "
            f"Solo Account: {self.settings['soloAccount']}, "
            f"BB Collect: {self.settings['BBCollectResources']}, "
            f"Clock Tower Boost: {self.settings['BBActivateCTBoost']}, "
            f"Gem Cooldown: {self.settings['gemCooldown']}")

        # If there's an existing thread, wait for it to finish before creating a new one
        if self.bot_thread and self.bot_thread.isRunning():
            print("Waiting for the previous bot thread to finish...")
            self.bot_thread.wait()

        # Here you would add the logic to start the bot with these configurations
        #* pass the variables to the functions that need them
        # Example: You might want to call bb_attack_loop() here or modify it to accept parameters based on the GUI settings
        enable_gem_cooldown = enable_gem_cooldown
        attack_only_no_cg = attack_only_no_cg
        clan_games_mode = clan_games_mode

        # main(enable_gem_cooldown, clan_games_mode, attack_only_no_cg)
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