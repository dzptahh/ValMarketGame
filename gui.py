# valorant_night_market/gui.py
from tkinter import *
from tkinter import messagebox
from player import Player
from market import Market
from stats_manager import StatsManager
import time
import threading

class NightMarketApp:
    def __init__(self, master):
        self.master = master
        self.player = Player(balance=2000)
        self.market = Market()
        self.stats = StatsManager()
        self.market.generate_offers()

        self.time_left = 60
        self.timer_running = True

        self.create_widgets()
        self.update_timer()

    def create_widgets(self):
        self.balance_label = Label(self.master, text=f"Balance: {self.player.balance} VP", font=("Arial", 16))
        self.balance_label.pack(pady=10)

        self.timer_label = Label(self.master, text=f"Time Left: {self.time_left}s", font=("Arial", 14))
        self.timer_label.pack(pady=5)

        self.skin_frame = Frame(self.master)
        self.skin_frame.pack(pady=20)

        self.display_skins()

        self.add_money_button = Button(self.master, text="Add 500 VP", command=self.add_money)
        self.add_money_button.pack(pady=5)

        self.inventory_button = Button(self.master, text="Show Inventory", command=self.show_inventory)
        self.inventory_button.pack(pady=5)

    def display_skins(self):
        for widget in self.skin_frame.winfo_children():
            widget.destroy()

        for idx, skin in enumerate(self.market.available_skins):
            frame = Frame(self.skin_frame, bd=2, relief=GROOVE)
            frame.grid(row=idx//3, column=idx%3, padx=10, pady=10)

            name_label = Label(frame, text=skin.name, font=("Arial", 12))
            name_label.pack()

            price_label = Label(frame, text=f"{skin.discounted_price} VP ({skin.rarity})")
            price_label.pack()

            buy_button = Button(frame, text="Buy", command=lambda s=skin: self.buy_skin(s))
            buy_button.pack()

    def buy_skin(self, skin):
        success = self.player.purchase_skin(skin)
        if success:
            self.stats.record_purchase(skin)
            self.update_balance()
            messagebox.showinfo("Success", f"You bought {skin.name} for {skin.discounted_price} VP!")
        else:
            messagebox.showerror("Error", "Not enough balance!")

    def update_balance(self):
        self.balance_label.config(text=f"Balance: {self.player.balance} VP")

    def add_money(self):
        self.player.add_money(500)
        self.update_balance()

    # gui.py
    def show_inventory(self):
        inventory_window = Toplevel(self.master)  # Create a new window for inventory
        inventory_window.title("Your Inventory")
        
        # If inventory is empty
        if not self.player.inventory:
            no_inventory_label = Label(inventory_window, text="Your inventory is empty!", font=("Arial", 14))
            no_inventory_label.pack(pady=10)
            return

        # Create a frame for displaying skins
        inventory_frame = Frame(inventory_window)
        inventory_frame.pack(padx=20, pady=20)

        # Display each skin with name and price
        for idx, skin in enumerate(self.player.inventory):
            frame = Frame(inventory_frame, bd=2, relief=GROOVE)
            frame.grid(row=idx//3, column=idx%3, padx=10, pady=10)

            # Display skin name and price
            name_label = Label(frame, text=skin.name, font=("Arial", 12))
            name_label.pack()

            price_label = Label(frame, text=f"{skin.discounted_price} VP", font=("Arial", 12))
            price_label.pack()

        # Add close button
        close_button = Button(inventory_window, text="Close", command=inventory_window.destroy)
        close_button.pack(pady=10)

    def update_timer(self):
        if self.time_left > 0 and self.timer_running:
            self.time_left -= 1
            self.timer_label.config(text=f"Time Left: {self.time_left}s")
            self.master.after(1000, self.update_timer)
        else:
            self.timer_running = False
            self.stats.save_data(self.player)
            messagebox.showinfo("Time's Up!", f"Game Over! You spent {self.player.total_spent} VP.")
            self.master.quit()
