import main

import unittest
from unittest.mock import patch
import pygame


class GameTests(unittest.TestCase):

    @patch('game.stop_game')
    def test_game_start(self, test_patch):
        """проверяем работает ли остановка игры при health = 0"""
        test_patch.return_value = 'win_test'
        main.health = 0
        self.assertEqual(main.run_game(), 'win_test')


if __name__ == '__main__':
    unittest.main
