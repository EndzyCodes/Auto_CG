# Existing imports and function definitions remain unchanged

# Add PyQt6 imports at the beginning of your file
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QPushButton
# from Functions import *

class ClashOfClansBotGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(500, 500)  # Set the fixed size of the window (width, height)
        layout = QVBoxLayout()

        self.gemCooldownCheckbox = QCheckBox("Gem Challenge Cooldown")
        layout.addWidget(self.gemCooldownCheckbox)

        self.clanGamesCheckbox = QCheckBox("Participate in Clan Games Challenges")
        layout.addWidget(self.clanGamesCheckbox)

        self.attackOnlyCheckbox = QCheckBox("Attack Only, No Clan Games")
        layout.addWidget(self.attackOnlyCheckbox)

        self.attackOnlyCheckbox = QCheckBox("Enable Attack")
        layout.addWidget(self.EnableAttackCheckbox)

        self.startButton = QPushButton("Start Bot")
        self.startButton.clicked.connect(self.startBot)
        layout.addWidget(self.startButton)

        self.setLayout(layout)
        self.setWindowTitle('Clash of Clans Bot Configuration')

    def startBot(self):
        gem_cooldown = self.gemCooldownCheckbox.isChecked()
        participate_in_clan_games = self.clanGamesCheckbox.isChecked()
        attack_only = self.attackOnlyCheckbox.isChecked()

        # Here you would add the logic to start the bot with these configurations
        #* Pass the gem_cooldown state to the purge_challenge function
        purge_challenge(gem_cooldown=gem_cooldown)
        bb_attack_loop(attack_only=attack_only)
        print(f"Starting bot with configurations: Gem Cooldown: {gem_cooldown}, Clan Games: {participate_in_clan_games}, Attack Only: {attack_only}")
        # Example: You might want to call bb_attack_loop() here or modify it to accept parameters based on the GUI settings

# if __name__ == '__main__':
#     app = QApplication([])
#     ex = ClashOfClansBotGUI()
#     ex.show()
#     app.exec()
    