# Clash of Clans Automation Script

## Overview

This repository contains a sophisticated Python automation script tailored for the popular mobile game "Clash of Clans." The script is designed to automate various in-game tasks by controlling the game window on a desktop environment using advanced techniques such as image recognition and Optical Character Recognition (OCR).

## Key Features

- **Automated Gameplay Tasks**: Automates repetitive in-game activities such as resource collection, attacking, troop boosting, and managing daily rewards.

- **Advanced Image Recognition**: Employs image recognition to intelligently interact with game UI elements.

- **Detailed Logging and Debugging**: Provides comprehensive logging to help trace the script's actions and facilitate effective troubleshooting.

- **OCR Capabilities**: Utilizes OCR to read and interpret text from the game's interface, enhancing the automation's decision-making processes.

## Installation

### Prerequisites

- Python installed on your system.

- Tesseract-OCR installed and configured.

### Required Libraries

Install the necessary Python libraries using pip:

pip install pyautogui pygetwindow win32gui pytesseract pillow colorlog keyboard


### Setup

1. **Configure Tesseract-OCR**:

   - Ensure that the path to Tesseract-OCR is correctly set in `Functions.py`.

2. **Adjust Game Window Title**:

   - Modify the `window_title` variable in `Functions.py` to match the title of your Clash of Clans game window.

## Usage

### Running the Script

1. Open your Clash of Clans game and ensure it is in the foreground on your desktop.

2. Execute the script from your command line or IDE:

python main.py

The script will automatically take control of the game window and start executing the predefined automation tasks.

### Customization

You can tailor the script to better fit your needs by modifying functions in `main.py` and `Functions.py`. This allows you to add new tasks or alter existing automation behaviors.

## Important Notes

- **Supervision**: It is recommended to supervise the script during execution to ensure it operates correctly and to intervene if necessary.

- **Game Updates**: Be aware that updates to the game may change UI elements, necessitating updates to the script's image assets and recognition logic.


## Conclusion

This automation script offers a powerful tool for Clash of Clans players, significantly reducing the manual effort required for routine game activities. Enjoy automating the mundane and focusing more on strategic gameplay! 🚀

---

For any issues or contributions, please feel free to open an issue or a pull request. Happy gaming! 🎮
