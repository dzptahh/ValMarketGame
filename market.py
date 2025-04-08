import random
from skin import Skin  # Assuming the Skin class is defined
import csv
class Market:
    def __init__(self, skin_file="valorant-skins.csv"):
        self.available_skins = []
        self.skin_names = self.load_skin_names(skin_file)  # Load skin names from the file
        self.rarity_pool = ["Common", "Rare", "Epic", "Legendary"]
        self.skin_data = self.load_skin_data("valorant-skins.csv") # Load skin data from CSV

    def load_skin_names(self, file_path):
        """Loads skin names from a text file (one name per line)."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                names = [line.strip() for line in file if line.strip()]
            return names
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}. Please create this file with skin names.")
            return []

    def load_skin_data(self, file_path):
        """Loads skin data from a CSV file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                skin_data = list(reader)  # Store the data as a list of dictionaries
                return skin_data
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}. Please create the file.")
            return []

    def generate_offers(self, count=6):
        self.available_skins = []
        if not self.skin_names:
            print("Error: No skin names available.  Please check the skin names file.")
            return  # Exit,  the rest of the method should not execute

        for _ in range(count):
            name = random.choice(self.skin_names)
            rarity = random.choice(self.rarity_pool)
            # changed to random choice and get name and price
            skin_data = random.choice(self.skin_data)
            price = int(skin_data['Price'])
            skin = Skin(name, price, rarity)  # Base price will be set by the Skin class
            skin.discounted_price = skin.calculate_discount_price()
            self.available_skins.append(skin)

    def refresh_skin(self, index):
        """Regenerate only the selected skin (at the given index) using data from the file."""
        if not self.skin_names:
            print("Error: No skin names loaded. Cannot refresh skin.")
            return

        if 0 <= index < len(self.available_skins):
            name = random.choice(self.skin_names)
            rarity = random.choice(self.rarity_pool)
            # changed to random choice and get name and price
            skin_data = random.choice(self.skin_data)
            price = int(skin_data['Price'])
            new_skin = Skin(name, price, rarity)  # Base price will be set by the Skin class
            new_skin.discounted_price = new_skin.calculate_discount_price()
            self.available_skins[index] = new_skin
        else:
            print(f"Error: Invalid index {index} for refreshing skin.")
