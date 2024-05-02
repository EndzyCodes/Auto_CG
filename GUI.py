import json
from Functions import setlog, get_coc_window, window_title
from bb_funcs import bb_attack_loop
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QPushButton, QGroupBox, QTabWidget, QRadioButton, QToolTip
from PyQt6.QtCore import QThread, pyqtSignal, Qt, QTimer

# def main(attack_only_no_cg=False,
#         enable_gem_cooldown=False,
#         clan_games_mode=False):

#     bb_attack_loop(attack_only_no_cg=attack_only_no_cg, clan_games_mode=clan_games_mode, gem_cooldown=enable_gem_cooldown)
def colorize_text(text, color):
    """
    Function to wrap text with ANSI color codes.
    """
    colors = {
        'blue': '\033[94m',   # Blue color
        'green': '\033[92m',  # Green color
        'red': '\033[91m'     # Red color
    }
    end_color = '\033[0m'  # Reset color to default
    return f"{colors[color]}{text}{end_color}"

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
        self.settings = {"gemCooldown": False, "clanGames": False, "attackOnly": False, "BBCollectResources": False, "BBActivateCTBoost": False} # Default settings
        self.loadSettings()
        self.bot_thread = None

    def initUI(self):
        self.setWindowTitle('Clash of Clans Bot Configuration')
        self.setFixedSize(480, 550) # Set the fixed size of the window (width, height)
        # this is the main window
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setGeometry(10, 10, 465, 470) # x, y, width, height of the tabs
        # self.tab_widget.currentChanged.connect(self.tabChanged)  # Connect tab change event

        #* Create the widgets for each tab
        self.clan_games_tab = QWidget()
        self.bb_attack_tab = QWidget()
        self.main_village_tab = QWidget()

        #* create the tabs here
        self.tab_widget.addTab(self.clan_games_tab, "Clan Games")
        self.tab_widget.addTab(self.bb_attack_tab, "Builder Base")
        self.tab_widget.addTab(self.main_village_tab, "Main Village")

        #* Setup the tab contents here
        self.setupClanGamesTab()
        self.setupBuilderBaseTab()
        self.setupBottomButtons()

        #* Set tooltips here
        # Clan games tab
        self.gemCooldownCheckbox.setToolTip('Spend gems to speed up a challenge purge.')
        self.clanGamesRadio.setToolTip('Clan Games and BB attack to complete challenges.')
        self.attackOnlyRadio.setToolTip('BB attack only, no main village attacks or clan games.')
        # Builder Base tab
        self.BBChkCollectResources.setToolTip('Collect resources in Builder Base.')
        self.BBChkActivateCTBoost.setToolTip('Activate Clocktower boost in Builder Base.')

        #* Connect hover events to show tooltips after a delay
        # Clan games tab
        self.connectHoverEvents(self.gemCooldownCheckbox)
        self.connectHoverEvents(self.clanGamesRadio)
        self.connectHoverEvents(self.attackOnlyRadio)
        # Builder Base  tab
        self.connectHoverEvents(self.BBChkCollectResources)
        self.connectHoverEvents(self.BBChkActivateCTBoost)

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

    def setupClanGamesTab(self):
        # self.removeClanGamesTabWidgets()  # Clear previous widgets if any
        #* Clan Games Settings group box
        self.CGsettings_group_box = QGroupBox("Clan Games Settings", self.clan_games_tab)
        self.CGsettings_group_box.setGeometry(15, 10, 200, 100)

        self.gemCooldownCheckbox = QCheckBox("Gem Challenge Cooldown", self.CGsettings_group_box)
        self.gemCooldownCheckbox.move(10, 20)

        #* Modes group box
        modes_group_box = QGroupBox("Modes", self.clan_games_tab)
        modes_group_box.setGeometry(15, 130, 200, 100)

        self.clanGamesRadio = QRadioButton("Clan Games Mode", modes_group_box)
        self.clanGamesRadio.move(10, 20)
        self.attackOnlyRadio = QRadioButton("Attack Only, No Clan Games", modes_group_box)
        self.attackOnlyRadio.move(10, 45)

    def removeClanGamesTabWidgets(self):
        # if hasattr(self, 'CGsettings_group_box'):
        self.CGsettings_group_box.setParent(None)
        self.CGsettings_group_box.deleteLater()
        #* delete the widgets here
        del self.gemCooldownCheckbox

        del self.clanGamesRadio
        del self.attackOnlyRadio

    def setupBuilderBaseTab(self):
        bb_attack_tab = QWidget()
        bb_attack_layout = QVBoxLayout()
        bb_attack_tab.setLayout(bb_attack_layout)

        self.BBsettings_group_box = QGroupBox("Collect & Activate", self.bb_attack_tab)
        self.BBsettings_group_box.setGeometry(15, 15, 200, 100)

        self.BBChkCollectResources = QCheckBox("Collect Resources", self.BBsettings_group_box)
        self.BBChkCollectResources.move(10, 20)

        self.BBChkActivateCTBoost = QCheckBox("Activate Clocktower Boost", self.BBsettings_group_box)
        self.BBChkActivateCTBoost.move(10, 45)

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
        print("Loading settings...")
        try:
            with open("settings.json", "r") as file:
                self.settings = json.load(file)
                print("Settings loaded successfully:", self.settings)
                # Set checkbox states based on loaded settings
                self.gemCooldownCheckbox.setChecked(self.settings.get("gemCooldown", False))
                self.clanGamesRadio.setChecked(self.settings.get("clanGames", False))
                self.attackOnlyRadio.setChecked(self.settings.get("attackOnly", False))

                self.BBChkCollectResources.setChecked(self.settings.get("BBCollectResources", False))
                self.BBChkActivateCTBoost.setChecked(self.settings.get("BBActivateCTBoost", False))

        except FileNotFoundError:
            print("Settings file not found. Using default settings.")
        except json.JSONDecodeError:
            print("Error loading settings file. Using default settings.")

    def saveSettings(self):
        try:
            #* Clan Games tab
            self.settings["gemCooldown"] = self.gemCooldownCheckbox.isChecked()
            self.settings["clanGames"] = self.clanGamesRadio.isChecked()
            self.settings["attackOnly"] = self.attackOnlyRadio.isChecked()
            #* Builder Base tab
            self.settings["BBCollectResources"] = self.BBChkCollectResources.isChecked()
            self.settings["BBActivateCTBoost"] = self.BBChkActivateCTBoost.isChecked()

            with open("settings.json", "w") as file:
                json.dump(self.settings, file)

            print("Settings saved successfully.")
        except Exception as e:
            print(f"Error saving settings: {e}")

    def startBot(self):
        enable_gem_cooldown = self.gemCooldownCheckbox.isChecked()
        # clan_games_mode = self.clanGamesCheckbox.isChecked()
        # attack_only_no_cg = self.attackOnlyCheckbox.isChecked()
        clan_games_mode = self.clanGamesRadio.isChecked()
        attack_only_no_cg = self.attackOnlyRadio.isChecked()
        self.saveSettings()  # Save settings when starting the bot

        gem_cooldown_color = 'green' if self.settings['gemCooldown'] else 'red'
        clan_games_color = 'green' if self.settings['clanGames'] else 'red'
        attack_only_color = 'green' if self.settings['attackOnly'] else 'red'
        bb_collect_color = 'green' if self.settings['BBCollectResources'] else 'red'
        ct_boost_color = 'green' if self.settings['BBActivateCTBoost'] else 'red'

        # Construct the colored output message
        output_message = (
            f"Starting bot with configurations: "
            f"Gem Cooldown: {colorize_text(self.settings['gemCooldown'], gem_cooldown_color)}, "
            f"Clan Games: {colorize_text(self.settings['clanGames'], clan_games_color)}, "
            f"Attack Only: {colorize_text(self.settings['attackOnly'], attack_only_color)}, "
            f"BB Collect: {colorize_text(self.settings['BBCollectResources'], bb_collect_color)}, "
            f"Clock Tower Boost: {colorize_text(self.settings['BBActivateCTBoost'], ct_boost_color)}"
        )

        print(output_message)

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