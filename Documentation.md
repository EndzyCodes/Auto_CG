# Clash of Clans Bot Documentation

## Project Structure

The project is organized into features, each contained in its own directory under `src/features/`. The main features are:

- Clan Games
- Main Village
- Builder Base
- Auto Collect

Each feature has its own `__init__.py` file that defines what is exported from that feature.

## Using Features

To use a feature in your main script, import it like this:

```python
from src.features.clan_games import run_clan_games
from src.features.main_village import run_main_village
from src.features.builder_base import run_builder_base
from src.features.collect_resources import run_auto_collect
```

Now you can use these functions directly:

```python
run_clan_games()
run_main_village()
run_builder_base()
run_auto_collect()
```

## Extending Features

To add new functionality to a feature:

1. Add the new function to the appropriate file in the feature's directory.
2. Update the feature's `__init__.py` file to export the new function.

For example, if you add a new function `optimize_army` to the main village feature:

1. Add the function to `src/features/main_village/mv_utils.py` or `mv_main.py`.
2. Update `src/features/main_village/__init__.py`:

```python
from .mv_main import run_main_village, optimize_army
__all__ = ['run_main_village', 'optimize_army']
```

3. Now you can import and use this new function in your main script:

```python
from src.features.main_village import run_main_village, optimize_army
# Use the functions
run_main_village()
optimize_army()
```

## Configuration

Global configuration variables are stored in `src/config/settings.py`. These include:

- `assets_path`: Path to the assets directory
- `window_title`: Title of the Clash of Clans window

To use these in your code, import them from the config:

python
from src.config.settings import assets_path, window_title


## Utility Functions

Common utility functions are stored in the `src/Functions/` directory. These include:

- Image detection functions
- Click utilities
- Window management functions
- Logging utilities

Import these as needed in your feature modules.

## Running the Bot

The main entry point for the bot is `main.py`. This file should import and use the features as needed.

## GUI

The bot includes a GUI created with PyQt6. The GUI code is located in `GUI.py`.

## Maintenance

When updating or adding features:

1. Keep each feature self-contained in its directory.
2. Update the `__init__.py` file for the feature if you add new functions that should be accessible from outside the feature.
3. Use the utility functions from `src/Functions/` for common tasks.
4. Update this documentation if you make significant changes to the project structure or add new features.
