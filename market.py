import random
from skin import Skin
import csv
class Market:
    def __init__(self, skin_file="valorant-skins.csv"):
        self.available_skins = []
        self.skin_names = self.load_skin_names(skin_file)
        self.rarity_pool = ["Common", "Rare", "Epic", "Legendary"]
        self.skin_data = self.load_skin_data(skin_file)
        self.generate_offers()

    def load_skin_names(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                if 'Name' not in reader.fieldnames:
                    print(f"Error: The CSV file '{file_path}' is missing the 'Name' column.")
                    return []
                names = [row['Name'] for row in reader]
            return names
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}. Please create this file with skin names.")
            return []

    def load_skin_data(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                return list(reader)
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}. Please create the file.")
            return []

    def generate_offers(self, count=6):
        self.available_skins = []
        if not self.skin_names:
            print("Error: No skin names available.  Please check the skin names file.")
            return

        for _ in range(count):
            name = random.choice(self.skin_names)
            rarity = random.choice(self.rarity_pool)
            if skin_data := next(
                (data for data in self.skin_data if data['Name'] == name), None
            ):
                price = int(skin_data['Price'])
                skin = Skin(name, price, rarity)
                skin.discounted_price = skin.calculate_discount_price()
                self.available_skins.append(skin)
            else:
                print(f"Warning: Skin data not found for '{name}'. Skipping.")

    def refresh_skin(self, index):
        if not self.skin_names:
            print("Error: No skin names loaded. Cannot refresh skin.")
            return

        if 0 <= index < len(self.available_skins):
            name = random.choice(self.skin_names)
            skin_data = next((data for data in self.skin_data if data['Name'] == name), None)
            rarity = random.choice(self.rarity_pool)
            if skin_data:
                price = int(skin_data['Price'])
                new_skin = Skin(name, price, rarity)
                new_skin.discounted_price = new_skin.calculate_discount_price()
                self.available_skins[index] = new_skin
            else:
                print(f"Warning: Skin data not found for '{name}'. Skipping refresh.")
        else:
            print(f"Error: Invalid index {index} for refreshing skin.")
