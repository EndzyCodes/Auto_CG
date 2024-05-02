import json
from Functions import setlog, get_coc_window, window_title
from bb_funcs import bb_attack_loop
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QPushButton, QGroupBox, QTabWidget
from PyQt6.QtCore import QThread, pyqtSignal

# def main(attack_only_no_cg=False,
#         enable_gem_cooldown=False,
#         clan_games_mode=False):

#     bb_attack_loop(attack_only_no_cg=attack_only_no_cg, clan_games_mode=clan_games_mode, gem_cooldown=enable_gem_cooldown)
def main(gem_cooldown,
        clan_games_mode,
        attack_only_no_cg):

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
        self.settings = {"gemCooldown": False, "clanGames": False, "attackOnly": False} # Default settings
        self.loadSettings()
        self.bot_thread = None

    def initUI(self):
        self.setWindowTitle('Clash of Clans Bot Configuration')
        self.setFixedSize(500, 500)  # Set the fixed size of the window (width, height)
        # this is the main window
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setGeometry(10, 10, 480, 350) # x, y, width, height
        self.tab_widget.currentChanged.connect(self.tabChanged)  # Connect tab change event

        #* Create the widgets for each tab
        self.clan_games_tab = QWidget()
        self.bb_attack_tab = QWidget()
        self.main_village_tab = QWidget()

        #* add/call tabs here to be shown on the GUI
        self.tab_widget.addTab(self.clan_games_tab, "Clan Games")
        self.tab_widget.addTab(self.bb_attack_tab, "BB Attack")
        self.tab_widget.addTab(self.main_village_tab, "Main Village")

        # Add "Save Settings" button
        self.saveSettingsButton = QPushButton("Save Settings", self)
        self.saveSettingsButton.move(310, 420)
        self.saveSettingsButton.resize(120, 40)
        self.saveSettingsButton.clicked.connect(self.saveSettings)

        self.startButton = QPushButton("Start Bot", self)
        self.startButton.move(30, 420)
        self.startButton.resize(120, 40)
        self.startButton.clicked.connect(self.startBot)  # Connect the button to startBot method

        self.stopButton = QPushButton("Stop Bot", self)
        self.stopButton.move(170, 420)
        self.stopButton.resize(120, 40)
        self.stopButton.clicked.connect(self.stopBot)  # Connect the button to stopBot method


    def tabChanged(self, index):
        if index == 0:  # Clan Games Tab
            self.setupClanGamesTab()
        elif index == 1:  # BB Attack Tab
            self.setupBBAttackTab()
        elif index == 2:  # Main Village Tab
            self.setupMainVillageTab()
        else:
            self.removeClanGamesTabWidgets()
            #  later add here for other tabs
            # TODO make remove widgets functions for other tabs like the def removeClanGamesTabWidgets(self)

    def setupClanGamesTab(self):
        # self.removeClanGamesTabWidgets()  # Clear previous widgets if any
        x_pos = 10
        self.CGsettings_group_box = QGroupBox("Clan Games Settings", self.clan_games_tab)
        self.CGsettings_group_box.setGeometry(15, 15, 200, 100)

        self.gemCooldownCheckbox = QCheckBox("Gem Challenge Cooldown", self.CGsettings_group_box)
        self.gemCooldownCheckbox.move(x_pos, 20)

        self.clanGamesCheckbox = QCheckBox("Clan Games Mode", self.CGsettings_group_box)
        self.clanGamesCheckbox.move(x_pos, 45)

        self.attackOnlyCheckbox = QCheckBox("Attack Only, No Clan Games", self.CGsettings_group_box)
        self.attackOnlyCheckbox.move(x_pos, 70)

    def removeClanGamesTabWidgets(self):
        # if hasattr(self, 'CGsettings_group_box'):
        self.CGsettings_group_box.setParent(None)
        self.CGsettings_group_box.deleteLater()
        #* delete the widgets here
        del self.gemCooldownCheckbox
        del self.clanGamesCheckbox
        del self.attackOnlyCheckbox

    def setupBBAttackTab(self):
        bb_attack_tab = QWidget()
        bb_attack_layout = QVBoxLayout()
        bb_attack_tab.setLayout(bb_attack_layout)

        # Add BB Attack tab content here...

        # self.tab_widget.addTab(bb_attack_tab, "BB Attack")

    def setupMainVillageTab(self):
        main_village_tab = QWidget()
        main_village_layout = QVBoxLayout()
        main_village_tab.setLayout(main_village_layout)

        # Add Main Village tab content here...

        # self.tab_widget.addTab(main_village_tab, "Main Village")

    def loadSettings(self):
        print("Loading settings...")
        try:
            with open("settings.json", "r") as file:
                self.settings = json.load(file)
                print("Settings loaded successfully:", self.settings)
                # Set checkbox states based on loaded settings
                self.gemCooldownCheckbox.setChecked(self.settings.get("gemCooldown", False))
                self.clanGamesCheckbox.setChecked(self.settings.get("clanGames", False))
                self.attackOnlyCheckbox.setChecked(self.settings.get("attackOnly", False))

        except FileNotFoundError:
            print("Settings file not found. Using default settings.")
        except json.JSONDecodeError:
            print("Error loading settings file. Using default settings.")

    def saveSettings(self):
        try:
            self.settings["gemCooldown"] = self.gemCooldownCheckbox.isChecked()
            self.settings["clanGames"] = self.clanGamesCheckbox.isChecked()
            self.settings["attackOnly"] = self.attackOnlyCheckbox.isChecked()

            with open("settings.json", "w") as file:
                json.dump(self.settings, file)

            print("Settings saved successfully.")
        except Exception as e:
            print(f"Error saving settings: {e}")

    def startBot(self):
        enable_gem_cooldown = self.gemCooldownCheckbox.isChecked()
        clan_games_mode = self.clanGamesCheckbox.isChecked()
        attack_only_no_cg = self.attackOnlyCheckbox.isChecked()
        self.saveSettings()  # Save settings when starting the bot

        print(f"Starting bot with configurations: Gem Cooldown: {self.settings['gemCooldown']}, Clan Games: {self.settings['clanGames']}, Attack Only: {self.settings['attackOnly']}")

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