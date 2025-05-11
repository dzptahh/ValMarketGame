from player import Player
from market import Market
from game_manager import GameManager
from stats_manager import StatsManager
from tkinter import Tk
from gui import NightMarketApp 

if __name__ == "__main__":
    root = Tk()
    root.title("Valorant Night Market")
    root.geometry("1000x650")
    root.geometry("800x750")

    root.configure(bg="#FFFDF7")
    app = NightMarketApp(root)
    root.mainloop()
