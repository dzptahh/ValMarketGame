from tkinter import *
import tkinter as tk
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
from PIL import Image, ImageTk  # Ensure you import these for image handling

class NightMarketApp(tk.Tk):  # Inherit from Tk instead of object
    def __init__(self):
        super().__init__()  # Call the Tk initialization
        self.player = Player(balance=10000)
        self.market = Market()
        self.stats = StatsManager()
        self.manager = GameManager(self.player, self.market, self.stats)
        self.market.generate_offers()
        self.time_left = 30
        self.timer_running = True
        self.game_over = False
        self.title("Valorant Night Market")
        self.login_page()
        self.resizable(True, True)
        self.update_timer()
           
    def login_page(self):
        self.geometry("1000x650")
        self.clear_frame()
        self.config(bg="#FFFDF7")
        # create login frame
        login_frame = tk.Frame(self, bd=0, highlightthickness=0, background="#FFFDF7", width=50)
        login_frame.grid(row=0, column=0, sticky="nsew", padx=80, pady=30)

        # create sign-in details
        text = tk.Label(login_frame, text="Sign in", font=('Futura', 36), fg='#3A405A', bg='#FFFDF7')
        text.pack(pady=5)

        # create register system
        username = tk.StringVar()
        password = tk.StringVar()

        # set username label and username entry
        username_label = tk.Label(login_frame, text="USERNAME", fg='#1F2933', padx=10, font="Futura", width=35, bg='#FFFDF7')
        username_label.pack(pady=5)
        self.entry_username = tk.Entry(login_frame, textvariable=username, fg='#1F2933', highlightbackground="#FFFDF7")
        self.entry_username.pack(pady=5, padx=10)

        # set password label and password entry
        password_label = tk.Label(login_frame, text="PASSWORD", fg='#1F2933', padx=10, font="Futura", bg='#FFFDF7')
        password_label.pack(pady=5)
        self.entry_password = tk.Entry(login_frame, textvariable=password, fg='#1F2933', show='*', highlightbackground="#FFFDF7")
        self.entry_password.pack(pady=5, padx=10)

        # set up the register button
        register_button = tk.Button(login_frame, width=10, height=1, text='Register', fg='#2CA58D', state=tk.DISABLED,
                                    command=self.handler, highlightbackground="#FFFDF7")

        # set up the trace on the username and password fields
        username.trace("w", lambda *args: self.toggle_button(register_button, username, password))
        password.trace("w", lambda *args: self.toggle_button(register_button, username, password))

        # pack the register button
        register_button.pack(pady=7)

        # set quit button
        self.quit = tk.Button(login_frame, text="log out", fg='#EA5455', command=self.destroy, highlightbackground="#FFFDF7")
        self.quit.pack(expand=False)

        # create image frame
        img_frame = tk.Frame(self, bd=0, highlightthickness=0, background="#c5f25b")
        img_frame.grid(row=0, column=1, sticky="nsew")

        # set image
        self.img = Image.open("Valorant-Gekko-Art.png")
        self.img = self.img.resize((800, 750))
        self.img = ImageTk.PhotoImage(self.img)

        # create canvas and display image
        canvas = tk.Canvas(img_frame, width=self.img.width(), height=self.img.height(), highlightthickness=0,
                           background="#c5f25b")
        canvas.create_image(0, 0, anchor="nw", image=self.img)
        canvas.grid(row=0, column=0, sticky="nsew", padx=5, pady=1)

        # configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        login_frame.grid_columnconfigure(0, weight=1)

        # set up the validation function
        def validate_input(new_value):
            return " " not in new_value

        # set up the validation command for the username and password entries
        validate_cmd = self.register(validate_input)
        self.entry_username.configure(validate="key", validatecommand=(validate_cmd, "%P"))
        self.entry_password.configure(validate="key", validatecommand=(validate_cmd, "%P"))

    @staticmethod
    def toggle_button(button, username, password):
        if username.get() != "" or password.get() != "":
            button.configure(state="normal")
        else:
            button.configure(state="disabled")

    def handler(self):
        if self.entry_username.get() != "" and self.entry_password.get() != "":
            self.player.name = self.entry_username.get()  # Set the player's name
            self.create_widgets()
        else:
            error_frame = tk.Frame(self, bg='white')
            error_frame.grid(row=4, column=1, sticky="nsew")

            fail = tk.Label(error_frame, text='Registration failed. Please enter all information.', fg='red')
            fail.grid(row=0, column=0)

            self.after(2000, fail.destroy)
            self.after(2000, error_frame.destroy)


    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def create_widgets(self):
        self.clear_frame()

        self.balance_label = tk.Label(self, text=f"Balance: {self.player.balance} VP", font=("Arial", 20), fg="#84BC9C", bg="#FFFDF7")
        self.balance_label.pack(pady=10)

        self.timer_label = tk.Label(self, text=f"Time Left: {self.time_left}s", font=("Arial", 28), fg="#F46197", bg="#FFFDF7")
        self.timer_label.pack(pady=5)

        self.skin_frame = tk.Frame(self, bg="#FFFDF7")
        self.skin_frame.pack(pady=20)

        self.display_skins()

        self.add_1000_button = tk.Button(self, text="Add 1000 VP (-5 sec)", command=lambda: self.add_money(1000, 5), highlightbackground="#FFFDF7", fg="#2CA58D")
        self.add_1000_button.pack(pady=5)

        self.add_2000_button = tk.Button(self, text="Add 2000 VP (-10 sec)", command=lambda: self.add_money(2000, 10), highlightbackground="#FFFDF7", fg="#2CA58D")
        self.add_2000_button.pack(pady=5)

        self.add_3000_button = tk.Button(self, text="Add 3000 VP (-15 sec)", command=lambda: self.add_money(3000, 15), highlightbackground="#FFFDF7", fg="#2CA58D")
        self.add_3000_button.pack(pady=5)

        self.inventory_button = tk.Button(self, text="Show Inventory", command=self.show_inventory, highlightbackground="#FFFDF7", fg="#2CA58D")
        self.inventory_button.pack(pady=5)

        quit_button = tk.Button(self, text="Quit", fg="red", command=self.destroy, highlightbackground="#FFFDF7")
        quit_button.pack()

        # Ensure that the timer is started after the widgets are created
        self.timer_running = True
    
    def start_timer(self):
        self.time_left = 30  # Reset the timer when game starts
        self.timer_running = True
        self.update_timer()
        
    def display_skins(self):
        for widget in self.skin_frame.winfo_children():
            widget.destroy()

        for idx, skin in enumerate(self.market.available_skins):
            # Updated: Added bg="#FFFDF7" to set background color
            frame = Frame(self.skin_frame, bd=2, relief=GROOVE, bg="#FFFDF7")
            frame.grid(row=idx // 3, column=idx % 3, padx=10, pady=10)

            name_label = Label(frame, text=skin.name, font=("Arial", 18), bg="#FFFDF7", fg="#0A2342")
            name_label.pack()

            price_label = Label(frame, text=f"Original Price: {skin.base_price} VP", font=("Arial", 10), bg="#FFFDF7")
            price_label.pack()

            discount_label = Label(frame, text=f"Discounted Price: {skin.discounted_price} VP", font=("Arial", 10), fg="#F46197", bg="#FFFDF7")
            discount_label.pack()

            discount_percentage = int((1 - (skin.discounted_price / skin.base_price)) * 100)
            discount_info_label = Label(frame, text=f"Discount: {discount_percentage}%", font=("Arial", 10), fg="#F46197", bg="#FFFDF7")
            discount_info_label.pack()

            # Updated: Set Buy button background
            buy_button = Button(frame, text="Buy", command=lambda s=skin, idx=idx: self.buy_skin(s, idx), fg="#0A2342", highlightbackground="#FFFDF7")
            buy_button.pack()

    def buy_skin(self, skin, box_index):
        if self.game_over:
            return
        if self.manager.process_purchase(skin):  # Ensure process_purchase deducts from balance
            self.stats.record_purchase(skin)
            self.custom_popup("Purchase Successful ✅", f"You bought {skin.name} for {skin.discounted_price} VP! 🔥")
            self.market.refresh_skin(box_index)
            new_skin = self.market.available_skins[box_index]
            self.update_skin_display(new_skin, box_index)
            self.update_balance()  # This ensures the balance gets updated in the UI
        else:
            self.custom_popup("Purchase Failed ❌", "Not enough balance! 💸")
            self.update_balance()


    def custom_popup(self, title, message):
        # Create a new top-level window for the popup
        popup = Toplevel(self)
        popup.title(title)
        popup.geometry("300x150")  # Set size for the popup (optional)

        # Add a label with the message
        label = Label(popup, text=message, font=("Arial", 12))
        label.pack(padx=20, pady=20)

        # Add an OK button to close the popup
        button = Button(popup, text="OK", command=popup.destroy)
        button.pack(pady=10)

        # This ensures that the main window is not interacted with while the popup is open
        self.wait_window(popup)  # Blocks further interaction with the main window until the popup is closed


        
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
        if self.timer_running:
            if self.time_left > 0:
                self.time_left -= 1
                # Update the timer label with the remaining time
                if hasattr(self, "timer_label"):
                    self.timer_label.config(text=f"Time Left: {self.time_left}s")
                self.after(1000, self.update_timer)  # Continue the timer update after 1 second
            else:
                self.timer_running = False  # Stop the timer
                self.game_over = True  # Flag to indicate game over
                # Collect the necessary data to pass to the game over screen
                total_spent = self.player.total_spent
                total_purchases = self.player.total_purchases
                total_score = self.player.calculate_score()

                # Call the function to show the game over screen and pass the stats
                self.show_game_over_screen(total_spent, total_purchases, total_score)


    def show_game_over_screen(self, total_spent, total_purchases, total_score):
        self.clear_frame()
        self.stats.save_data(self.player)

        # Create the widgets for the game over screen directly in the main window
        game_over_frame = Frame(self.master)
        game_over_frame.pack(pady=20, padx=20)
        game_over_frame.columnconfigure(0, weight=1)
        game_over_frame.columnconfigure(1, weight=1)

        # Left side for Leaderboard
        left_frame = Frame(game_over_frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        game_over_label = Label(left_frame, text="Game Over", font=("Arial", 24, "bold"), fg="#F46197")
        game_over_label.pack(pady=10)

        leaderboard_label = Label(left_frame, text="🏆 Leaderboard", font=("Arial", 18), fg="#2CA58D")
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

        leaderboard_text_label = Label(left_frame, text=summary_text, font=("Arial", 12), justify=LEFT, fg="#705D56")
        leaderboard_text_label.pack()

        # Right side for Summary and Graph
        right_frame = Frame(game_over_frame)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        summary_label = Label(right_frame, text="📊 Game Summary", font=("Arial", 18), fg="#D76A03")
        summary_label.pack(pady=5)

        summary_text = (
            f"Your Name: {self.player.name}\n"
            f"Total Spent: {total_spent} VP\n"
            f"Skins Bought: {total_purchases}\n"
            f"Final Score: {total_score} Points\n"
            f"Additional Money Added: {total_added_money} VP\n"
        )
        summary_text_label = Label(right_frame, text=summary_text, font=("Arial", 12), justify=LEFT, fg="#705D56")
        summary_text_label.pack()

        # Graph for Player Scores
        if leaderboard:
            fig, ax = plt.subplots(figsize=(5, 4))  # Adjusted size to make it more compact

            # Extract player names and scores
            player_names = [entry['name'] for entry in leaderboard]
            player_scores = [entry['score'] for entry in leaderboard]

            # Plot bar chart
            ax.bar(player_names, player_scores, color='#4CAF50')
            ax.set_title("Player Scores")
            ax.set_xlabel("Player Name")
            ax.set_ylabel("Score")

            # Rotate x-axis labels to 45° for better visibility and compactness
            ax.set_xticks(range(len(player_names)))
            ax.set_xticklabels(player_names, rotation=45, ha='right', fontsize=9)

            # Apply grid for better readability
            ax.grid(axis='y', linestyle='--', alpha=0.7)

            # Adjust layout to prevent label cutoff
            plt.tight_layout()

            # Embed the plot in the right frame
            canvas = FigureCanvasTkAgg(fig, master=right_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=10)
        else:
            no_data_label = Label(right_frame, text="No data available to plot.", font=("Arial", 12))
            no_data_label.pack(pady=10)

        close_button = Button(self, text="Close", command=self.destroy, highlightbackground="#FFFDF7", fg="#F46197")
        close_button.pack(pady=10)



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


            
    # def clear_frame(self):
    #     # Remove all widgets from the current frame to prepare for the next page
    #     for widget in self.winfo_children():
    #         widget.destroy()
    
if __name__ == '__main__':
    ui = NightMarketApp()
    ui.mainloop()  # Start the Tkinter event loop
