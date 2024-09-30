import unittest
from unittest.mock import patch
from src.Features.clan_games import run_clan_games

class TestClanGames(unittest.TestCase):
    @patch('src.features.clan_games.click_random_within_image')
    def test_run_clan_games(self, mock_click):
        # Set up any necessary mocks
        mock_click.return_value = True

        # Run the function
        result = run_clan_games()

        # Assert the expected behavior
        self.assertTrue(result)
        mock_click.assert_called()

if __name__ == '__main__':
    unittest.main()
