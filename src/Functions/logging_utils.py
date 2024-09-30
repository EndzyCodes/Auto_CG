import colorlog
import logging
from datetime import datetime

def setup_logging():
    log_formatter = colorlog.ColoredFormatter(
        '%(green)s[%(asctime)s]%(reset)s:%(log_color)s %(message)s%(reset)s', datefmt='%H:%M:%S',
        log_colors={
            'DEBUG': 'white',
            'INFO': 'cyan',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)

    logging.root.setLevel(logging.INFO)
    logging.root.addHandler(console_handler)

def setlog(string, log_level):
    # Define color codes
    color_reset = "\033[0m"
    success_color = "\033[92m" # green
    debug_color = "\033[97m"  # White
    error_color = "\033[91m"  # Red
    info_color = "\033[96m"   # Cyan
    warning_color = "\033[93m"  # Yellow
    heading_color = "\033[94m"
    purple_color = "\033[35m"
    # other colors
    # \033[30m - Black
    # \033[90m - Bright Black
    # \033[31m - Red
    # \033[91m - Bright Red
    # \033[32m - Green
    # \033[92m - Bright Green
    # \033[33m - Yellow
    # \033[93m - Bright Yellow
    # \033[34m - Blue
    # \033[94m - Bright Blue
    # \033[35m - Magenta/purple
    # \033[95m - Bright Magenta/purple
    # \033[36m - Cyan
    # \033[96m - Bright Cyan
    # \033[37m - White
    # Set color based on log_level
    if log_level == "success":
        color = success_color
    elif log_level == "debug":
        color = debug_color
    elif log_level == "error":
        color = error_color
    elif log_level == "info":
        color = info_color
    elif log_level == "warning":
        color = warning_color
    elif log_level == "heading":
        color = heading_color
    elif log_level == "purple":
        color = purple_color
    else:
        color = ""  # Default to no color if log_level is not recognized

    # Get current time
    current_time = datetime.now().strftime('%H:%M:%S')

    # Print formatted log message with time
    if log_level == "error":
        print(f"[{current_time}]: {color}[ERROR] {string}{color_reset}")
    else:
        print(f"[{current_time}]: {color}{string}{color_reset}")

setup_logging()
