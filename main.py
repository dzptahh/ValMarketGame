from player import Player
from market import Market
from game_manager import GameManager
from stats_manager import StatsManager
from tkinter import Tk
from gui import NightMarketApp
# def main():
#     player = Player()
#     market = Market()
#     stats = StatsManager()
#     game = GameManager(player, market, stats)
#     game.start_game()

if __name__ == "__main__":
    root = Tk()
    root.title("Valorant Night Market")
    root.geometry("800x600")
    app = NightMarketApp(root)
    root.mainloop()
