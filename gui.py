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
        self.player = Player(balance=10000)
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

        # Create the buttons to add VP with time penalty
        self.add_1000_button = Button(self.master, text="Add 1000 VP (-5 sec)", command=lambda: self.add_money(1000, 5))
        self.add_1000_button.pack(pady=5)

        self.add_2000_button = Button(self.master, text="Add 2000 VP (-10 sec)", command=lambda: self.add_money(2000, 10))
        self.add_2000_button.pack(pady=5)

        self.add_3000_button = Button(self.master, text="Add 3000 VP (-15 sec)", command=lambda: self.add_money(3000, 15))
        self.add_3000_button.pack(pady=5)

        self.inventory_button = Button(self.master, text="Show Inventory", command=self.show_inventory)
        self.inventory_button.pack(pady=5)

    def display_skins(self):
        # Clear any previous widgets (for refreshing the display)
        for widget in self.skin_frame.winfo_children():
            widget.destroy()

        # Display skins with discount information
        for idx, skin in enumerate(self.market.available_skins):
            frame = Frame(self.skin_frame, bd=2, relief=GROOVE)
            frame.grid(row=idx // 3, column=idx % 3, padx=10, pady=10)

            # Skin name label
            name_label = Label(frame, text=skin.name, font=("Arial", 12))
            name_label.pack()

            # Price and discount labels
            price_label = Label(frame, text=f"Original Price: {skin.base_price} VP", font=("Arial", 10))
            price_label.pack()

            discount_label = Label(frame, text=f"Discounted Price: {skin.discounted_price} VP", font=("Arial", 10))
            discount_label.pack()

            discount_percentage = int((1 - (skin.discounted_price / skin.base_price)) * 100)
            discount_info_label = Label(frame, text=f"Discount: {discount_percentage}%", font=("Arial", 10))
            discount_info_label.pack()

            # Button to buy skin
            buy_button = Button(frame, text="Buy", command=lambda s=skin: self.buy_skin(s))
            buy_button.pack()

    def custom_popup(self, title, message):
        popup = Toplevel(self.master)
        popup.title(title)
        popup.geometry("300x150")

        label = Label(popup, text=message, font=("Arial", 12))
        label.pack(pady=20)

        ok_button = Button(popup, text="OK", command=popup.destroy)
        ok_button.pack(pady=10)

        popup.transient(self.master)  # Keep the popup on top of the main window
        popup.grab_set()  # Disable interaction with the main window until the popup is closed
        self.master.wait_window(popup)  # Wait until the popup is closed before continuing
        
    def buy_skin(self, skin):
        if success := self.player.purchase_skin(skin):
            self.stats.record_purchase(skin)
            self.update_balance()
            self.custom_popup("Purchase Successful", f"You bought {skin.name} for {skin.discounted_price} VP!")
        else:
            self.custom_popup("Purchase Failed", "Not enough balance!")

    def update_balance(self):
        self.balance_label.config(text=f"Balance: {self.player.balance} VP")

    def add_money(self, amount, time_penalty):
        if self.player.balance + amount >= 0:  # Check to ensure that the player has enough balance
            self.player.balance += amount
            self.time_left -= time_penalty  # Decrease the time based on the penalty
            self.update_balance()
            messagebox.showinfo("Money Added", f"Added {amount} VP. Time penalty: {time_penalty} seconds.")
        else:
            messagebox.showwarning("Insufficient Balance", "You cannot add money. Please make a purchase first!")


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