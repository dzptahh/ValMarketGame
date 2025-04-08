from tkinter import *
from tkinter import messagebox
from player import Player
from market import Market
from stats_manager import StatsManager
import time
import threading
from tkinter.simpledialog import askstring
from game_manager import GameManager
import random
import io
import csv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
class NightMarketApp:
    def __init__(self, master):
        self.master = master
        self.player = Player(balance=10000)
        self.market = Market()
        self.stats = StatsManager()
        self.manager = GameManager(self.player, self.market, self.stats)
        self.market.generate_offers()

        self.time_left = 30
        self.timer_running = True
        self.game_over = False

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

        self.add_1000_button = Button(self.master, text="Add 1000 VP (-5 sec)", command=lambda: self.add_money(1000, 5))
        self.add_1000_button.pack(pady=5)

        self.add_2000_button = Button(self.master, text="Add 2000 VP (-10 sec)", command=lambda: self.add_money(2000, 10))
        self.add_2000_button.pack(pady=5)

        self.add_3000_button = Button(self.master, text="Add 3000 VP (-15 sec)", command=lambda: self.add_money(3000, 15))
        self.add_3000_button.pack(pady=5)

        self.inventory_button = Button(self.master, text="Show Inventory", command=self.show_inventory)
        self.inventory_button.pack(pady=5)
        
        quit_button = Button(self.master, text="Quit",fg="red", command=self.master.destroy)
        quit_button.pack()
        
    def display_skins(self):
        for widget in self.skin_frame.winfo_children():
            widget.destroy()

        for idx, skin in enumerate(self.market.available_skins):
            frame = Frame(self.skin_frame, bd=2, relief=GROOVE)
            frame.grid(row=idx // 3, column=idx % 3, padx=10, pady=10)

            name_label = Label(frame, text=skin.name, font=("Arial", 12))
            name_label.pack()

            price_label = Label(frame, text=f"Original Price: {skin.base_price} VP", font=("Arial", 10))
            price_label.pack()

            discount_label = Label(frame, text=f"Discounted Price: {skin.discounted_price} VP", font=("Arial", 10))
            discount_label.pack()

            discount_percentage = int((1 - (skin.discounted_price / skin.base_price)) * 100)
            discount_info_label = Label(frame, text=f"Discount: {discount_percentage}%", font=("Arial", 10))
            discount_info_label.pack()

            buy_button = Button(frame, text="Buy", command=lambda s=skin, idx=idx: self.buy_skin(s, idx))
            buy_button.pack()

    def buy_skin(self, skin, box_index):
        if self.game_over:
            return
        if self.manager.process_purchase(skin):
            self.stats.record_purchase(skin)
            self.custom_popup("Purchase Successful ✅", f"You bought {skin.name} for {skin.discounted_price} VP! 🔥")
            self.market.refresh_skin(box_index)
            new_skin = self.market.available_skins[box_index]
            self.update_skin_display(new_skin, box_index)
            self.update_balance()
        else:
            self.custom_popup("Purchase Failed ❌", "Not enough balance! 💸")
            self.update_balance()

    def custom_popup(self, title, message):
        popup = Toplevel(self.master)
        popup.title(title)
        popup.geometry("300x150")

        label = Label(popup, text=message, font=("Arial", 12))
        label.pack(pady=20)

        ok_button = Button(popup, text="OK", command=popup.destroy)
        ok_button.pack(pady=10)

        popup.transient(self.master)
        popup.grab_set()
        self.master.wait_window(popup)
        
    def update_skin_display(self, skin, box_index):
        skin_frame = self.skin_frame.winfo_children()[box_index]
        
        name_label = skin_frame.winfo_children()[0]
        price_label = skin_frame.winfo_children()[1]
        discount_label = skin_frame.winfo_children()[2]
        discount_info_label = skin_frame.winfo_children()[3]
        buy_button = skin_frame.winfo_children()[4]
        
        name_label.config(text=skin.name)
        price_label.config(text=f"Original Price: {skin.base_price} VP")
        discount_label.config(text=f"Discounted Price: {skin.discounted_price} VP")

        discount_percentage = int((1 - (skin.discounted_price / skin.base_price)) * 100)
        discount_info_label.config(text=f"Discount: {discount_percentage}%")

        buy_button.config(state=NORMAL)

    def update_balance(self):
        self.balance_label.config(text=f"Balance: {self.player.balance} VP")


    def add_money(self, amount, time_penalty):
        if self.player.balance + amount >= 0:
            self.player.balance += amount
            self.time_left -= time_penalty
            self.update_balance()
            messagebox.showinfo("Money Added", f"Added {amount} VP. Time penalty: {time_penalty} seconds.")
        else:
            messagebox.showwarning("Insufficient Balance", "You cannot add money. Please make a purchase first!")


    def show_inventory(self):
        inventory_window = Toplevel(self.master)
        inventory_window.title("Your Inventory")
        
        if not self.player.inventory:
            no_inventory_label = Label(inventory_window, text="Your inventory is empty!", font=("Arial", 14))
            no_inventory_label.pack(pady=10)
            return

        inventory_frame = Frame(inventory_window)
        inventory_frame.pack(padx=20, pady=20)

        for idx, skin in enumerate(self.player.inventory):
            frame = Frame(inventory_frame, bd=2, relief=GROOVE)
            frame.grid(row=idx//3, column=idx%3, padx=10, pady=10)

            name_label = Label(frame, text=skin.name, font=("Arial", 12))
            name_label.pack()

            price_label = Label(frame, text=f"{skin.discounted_price} VP", font=("Arial", 12))
            price_label.pack()

        close_button = Button(inventory_window, text="Close", command=inventory_window.destroy)
        close_button.pack(pady=10)

    def update_timer(self):
        if self.time_left > 0 and self.timer_running:
            self.time_left -= 1
            self.timer_label.config(text=f"Time Left: {self.time_left}s")
            self.master.after(1000, self.update_timer)
        else:
            self.timer_running = False
            self.game_over = True
            self.stats.save_data(self.player)
            total_spent = self.player.total_spent
            total_purchases = self.player.total_purchases
            total_score = self.player.calculate_score()
            self.show_game_over_screen(total_spent, total_purchases, total_score)

    def show_game_over_screen(self, total_spent, total_purchases, total_score):
        # Destroy all widgets in the main window
        for widget in self.master.winfo_children():
            widget.destroy()

        # Create the widgets for the game over screen directly in the main window
        game_over_frame = Frame(self.master)
        game_over_frame.pack(pady=20, padx=20)
        game_over_frame.columnconfigure(0, weight=1)
        game_over_frame.columnconfigure(1, weight=1)

        # Left side for Leaderboard
        left_frame = Frame(game_over_frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        game_over_label = Label(left_frame, text="Game Over", font=("Arial", 24, "bold"))
        game_over_label.pack(pady=10)

        leaderboard_label = Label(left_frame, text="🏆 Leaderboard", font=("Arial", 18))
        leaderboard_label.pack(pady=5)

        leaderboard = self.stats.get_top_scores()
        total_added_money = sum(item["Amount Added"] for item in self.stats.additional_money_record)

        summary_text = ""
        if not leaderboard:
            summary_text += "No scores available yet.\n"
        else:
            summary_text += "Top Scores:\n"
            for i, entry in enumerate(leaderboard):
                summary_text += f"{i+1}. {entry['name']}: {entry['score']} Points\n"

        leaderboard_text_label = Label(left_frame, text=summary_text, font=("Arial", 12), justify=LEFT)
        leaderboard_text_label.pack()

        # Right side for Summary and Graph
        right_frame = Frame(game_over_frame)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        summary_label = Label(right_frame, text="📊 Game Summary", font=("Arial", 18))
        summary_label.pack(pady=5)

        summary_text = (
            f"Your Name: {self.player.name}\n"
            f"Total Spent: {total_spent} VP\n"
            f"Skins Bought: {total_purchases}\n"
            f"Final Score: {total_score} Points\n"
            f"Additional Money Added: {total_added_money} VP\n"
        )
        summary_text_label = Label(right_frame, text=summary_text, font=("Arial", 12), justify=LEFT)
        summary_text_label.pack()

        # Graph for Total Spent
        fig, ax = plt.subplots(figsize=(6, 4))
        #ax.hist(self.stats.total_money_spent, bins=5)  # Example: Histogram of total spent
        # Instead of a histogram, let's plot a bar chart of total spent for each player in the leaderboard
        player_names = [entry['name'] for entry in leaderboard]
        player_scores = [entry['score'] for entry in leaderboard] # use score instead of total_money_spent
        ax.bar(player_names, player_scores)
        ax.set_title("Player Scores")
        ax.set_xlabel("Player Name")
        ax.set_ylabel("Score")
        canvas = FigureCanvasTkAgg(fig, master=right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

        close_button = Button(game_over_frame, text="Close", command=self.master.destroy, font=("Arial", 12), bg="#4CAF50", fg="white", padx=10, pady=5)
        close_button.grid(row=1, column=0, columnspan=2, pady=10)



    def close_game_over_screen(self):
        self.game_over_window.destroy()
        self.master.attributes("-alpha", 1.0)  # Restore full opacity to the main window
        
    def update_inventory_display(self):
        for widget in self.inventory_button.winfo_children():
            widget.destroy()

        inventory_window = Toplevel(self.master)
        inventory_window.title("Your Inventory")

        if not self.player.inventory:
            no_inventory_label = Label(inventory_window, text="Your inventory is empty!", font=("Arial", 12))
            no_inventory_label.pack(pady=10)
        else:
            inventory_frame = Frame(inventory_window)
            inventory_frame.pack(padx=20, pady=20)

            for idx, skin in enumerate(self.player.inventory):
                frame = Frame(inventory_frame, bd=2, relief=GROOVE)
                frame.grid(row=idx // 3, column=idx % 3, padx=10, pady=10)

                name_label = Label(frame, text=skin.name, font=("Arial", 10))
                name_label.pack()

                price_label = Label(frame, text=f"Price: {skin.discounted_price} VP", font=("Arial", 8))
                price_label.pack()

            close_button = Button(inventory_window, text="Close", command=inventory_window.destroy)
            close_button.pack(pady=10)
